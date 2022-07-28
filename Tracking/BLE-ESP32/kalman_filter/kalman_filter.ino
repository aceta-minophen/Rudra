#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLEAdvertisedDevice.h>
 
// Comment this line out for the final version (terse output in the serial monitor)
//#define VERBOSE

// Comment this out to re-enable connection signalling on pin 8
//#define CONNECT_SIGNALLING

BLECharacteristic *pCharacteristic;
 
// See the following for generating UUIDs:
// https://www.uuidgenerator.net/
 
#define SERVICE_UUID        "6012d087-05f8-41b0-90ed-07a75e80a104"
#define CHARACTERISTIC_UUID "73af693f-f43f-4997-817c-3c226530ad76"
#define DESCRIPTOR_UUID    "e8f45c7e-8be5-4918-bb84-467d3fd354aa"


#ifdef CONNECT_SIGNALLING
// That pin used to be 2, feature removed
const uint8_t LED_CONNECT_PIN = 7;    // Can be any other pin
#endif

const uint8_t LED_ON_PIN = 2; //PUT INTERNAL LED PIN HERE
const uint8_t MOTOR_PIN = 6; // PUT YOUR MOTOR'S PIN HERE

 
template <typename T, size_t N>
void show_address(const T (&address)[N])
{
  Serial.print(address[0], HEX);
  for (uint8_t i = 1; i < N; i++)
    Serial.printf(":%02x", address[i]);
}
 
 
class Monitor: public BLEServerCallbacks
{
public:
  static int16_t connection_id;

  // Motor state bits
  enum motor_states { ENABLED, ON };
  static bool motor_state;

  // Durations for motor ON and motor OFF in milliseconds
  // Note: make sure OFF_DELAY + ON_DELAY is equal to 1000!
  static constexpr uint32_t ON_DELAY = 300;
  static constexpr uint32_t OFF_DELAY = 700;

  /* dBm to distance parameters; How to update distance_factor 1.place the
   * phone at a known distance (2m, 3m, 5m, 10m) 2.average about 10 RSSI
   * values for each of these distances, Set distance_factor so that the
   * calculated distance approaches the actual distances, e.g. at 5m. */
  static constexpr float reference_power  = -50; //rssi reffrence 
  static constexpr float distance_factor = 3.5; 
   
  static constexpr int8_t motor_threshold = -65;
 
  uint8_t get_value() { return value++; }
  esp_err_t get_rssi() { return esp_ble_gap_read_rssi(remote_addr); }
 
  static float get_distance(const int8_t rssi)
  { return pow(10, (reference_power - rssi)/(10*distance_factor)); }
 
private:
    void onConnect(BLEServer* pServer, esp_ble_gatts_cb_param_t *param) 
    {
      // Update connection variables
    connection_id = param->connect.conn_id;
      memcpy(&remote_addr, param->connect.remote_bda, sizeof(remote_addr));

    // Install the RSSI callback
      BLEDevice::setCustomGapHandler(&Monitor::rssi_event);

#ifdef VERBOSE
      // Show new connection info
      Serial.printf("Connection #: %i, remote: ", connection_id);
    show_address(param->connect.remote_bda);
    Serial.printf(" [Callback installed]\n");
#endif

#ifdef CONNECT_SIGNALLING
      digitalWrite(LED_CONNECT_PIN, HIGH);
#endif
    }
 
    void onDisconnect(BLEServer* pServer)
    {
    Serial.printf("Connection #%i closed\n", connection_id);
    BLEDevice::setCustomGapHandler(nullptr);
    connection_id = -1;

#ifdef CONNECT_SIGNALLING
    digitalWrite(LED_CONNECT_PIN, LOW);
#endif
    }
 
    static void rssi_event(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param);
 
  static esp_bd_addr_t remote_addr;
  uint8_t value = 0;
};
 
int16_t Monitor::connection_id = -1;
bool Monitor::motor_state = 0;
esp_bd_addr_t Monitor::remote_addr = {};
 
void Monitor::rssi_event(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param)
{
    static int16_t rssi_average = 0;
 
#ifdef VERBOSE
  show_address(remote_addr);
#endif
    if (event == ESP_GAP_BLE_READ_RSSI_COMPLETE_EVT)
    {
        // Adjust damping_factor to lower values to have a more reactive response
        const float damping_factor = 0.8;
        rssi_average = rssi_average * damping_factor + 
          param->read_rssi_cmpl.rssi * (1 - damping_factor);

        // Flag motor as enabled, the loop function will turn it on in bursts
        if (rssi_average < motor_threshold)
          motor_state |= _BV(ENABLED);
      else
      {
        motor_state &= ~_BV(ENABLED);
        digitalWrite(MOTOR_PIN, LOW);
      }

#ifdef VERBOSE
    Serial.printf(", rssi=%hi, distance~=%g",
#else
    Serial.printf("%hi, %g\n",
#endif
      param->read_rssi_cmpl.rssi, get_distance(rssi_average)
    );
    }
#ifdef VERBOSE
  Serial.printf("\n");
#endif
}
 
Monitor monitor;
 
 
void setup()
{
  Serial.begin(9600);

  pinMode(MOTOR_PIN, OUTPUT);
  pinMode(LED_ON_PIN, OUTPUT);

#ifdef CONNECT_SIGNALLING
  pinMode(LED_CONNECT_PIN, OUTPUT);
#endif
 
  // Create the BLE Device
  BLEDevice::init("Esp-32");
 
  // Create the BLE Server
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(&monitor);
 
  // Create the BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);
 
  // Create a BLE Characteristic
  pCharacteristic = pService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_READ   |
    BLECharacteristic::PROPERTY_WRITE  |
    BLECharacteristic::PROPERTY_NOTIFY |
    BLECharacteristic::PROPERTY_INDICATE
  );
 
  // https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.descriptor.gatt.client_characteristic_configuration.xml
  // Create a BLE Descriptor
  pCharacteristic->addDescriptor(new BLEDescriptor(DESCRIPTOR_UUID));
 
  // Start the service
  pService->start();

  // Blink the LED on pin 8 three times
  for (uint8_t i = 0; i < 3; i++)
  {
    digitalWrite(LED_ON_PIN, HIGH);
    delay(500);
    digitalWrite(LED_ON_PIN, LOW);
    delay(500);
  }
 
  // Start advertising
  pServer->getAdvertising()->start();
  Serial.println("Waiting for incoming connections...");
}
 
void loop()
{
  static const uint32_t REFRESH_DELAY = 1000;
  static uint32_t next_detection;

  uint32_t current_time = millis();
  if (Monitor::connection_id != -1)
  {
    if (current_time - next_detection >= REFRESH_DELAY)
    {
      // Prepare for the next detection
      next_detection += REFRESH_DELAY;

      // Update the internal value (what for?)
      auto value = monitor.get_value();
      //Serial.printf("*** NOTIFY: %d ***\n", value);
      pCharacteristic->setValue(&value, sizeof(value));
      pCharacteristic->notify();
   
      // Request RSSI from the remote address
      if (monitor.get_rssi() != ESP_OK)
        Serial.println("RSSI request failed");
    }
  }

  // Let's turn the motor ON/OFF when enabled. The motor control pin will
  // toggle every time the threshold below is reached.
  static uint32_t motor_threshold;
  if (Monitor::motor_state & _BV(Monitor::ENABLED))
  {
    // Determine the next duration for either ON and OFF states
    const uint32_t next_threshold = Monitor::motor_state & _BV(Monitor::ON) ?
      Monitor::OFF_DELAY : Monitor::ON_DELAY;

    if (current_time - motor_threshold >= next_threshold)
    {
      // Toggle motor state
      Monitor::motor_state ^= _BV(Monitor::ON);
          digitalWrite(MOTOR_PIN,
            Monitor::motor_state & _BV(Monitor::ON) ? HIGH : LOW);
        }
  }
}
