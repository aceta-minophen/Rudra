#include <BLEDevice.h> //Header file for BLE 
#include <BLEClient.h>


static BLEUUID serviceUUID("adabfb00-6e7d-4601-bda2-bffaa68956ba"); //Service UUID of fitnessband obtained through nRF connect application 

static BLEUUID    charUUID("adabfb02-6e7d-4601-bda2-bffaa68956ba"); //Characteristic  UUID of fitnessband obtained through nRF connect application 

String My_BLE_Address = "c8:23:86:d7:2e:e7"; //Hardware Bluetooth MAC of my fitnessband, will vary for every band obtained through nRF connect application 

static BLERemoteCharacteristic* pRemoteCharacteristic;


BLEScan* pBLEScan; //Name the scanning device as pBLEScan

BLEScanResults foundDevices;


static BLEAddress *Server_BLE_Address;

String Scaned_BLE_Address;


boolean paired = false; //boolean variable to togge light


 


bool connectToserver (BLEAddress pAddress){

    

    BLEClient*  pClient  = BLEDevice::createClient();

    Serial.println(" - Created client");


    // Connect to the BLE Server.

    pClient->connect(pAddress);

    Serial.println(" - Connected to fitnessband");


    // Obtain a reference to the service we are after in the remote BLE server.

    BLERemoteService* pRemoteService = pClient->getService(serviceUUID);

    if (pRemoteService != nullptr)

    {

      Serial.println(" - Found our service");

      return true;

    }

    else{
      Serial.println(" - Error finding service");
      return false;
    }

    


    // Obtain a reference to the characteristic in the service of the remote BLE server.

    pRemoteCharacteristic = pRemoteService->getCharacteristic(charUUID);

    if (pRemoteCharacteristic != nullptr)

      Serial.println(" - Found our characteristic");


      return true;

}


class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks 

{

    void onResult(BLEAdvertisedDevice advertisedDevice) {

      Serial.printf("Scan Result: %s \n", advertisedDevice.toString().c_str());

      Server_BLE_Address = new BLEAddress(advertisedDevice.getAddress());

      

      Scaned_BLE_Address = Server_BLE_Address->toString().c_str();

      

    }

};



static void my_gap_event_handler(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t* param) {

  Serial.print("RSSI status");Serial.println(param->read_rssi_cmpl.status);
  Serial.print("RSSI ");Serial.println(param->read_rssi_cmpl.rssi);
  
  Serial.print("Address ");Serial.println(BLEAddress(param->read_rssi_cmpl.remote_addr).toString().c_str());
}



void setup() {

    Serial.begin(115200); //Start serial monitor 

    Serial.println("ESP32 BLE Server program"); //Intro message 


    BLEDevice::init("");

    pBLEScan = BLEDevice::getScan(); //create new scan

    pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks()); //Call the class that is defined above 

    pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster

    BLEDevice::setCustomGapHandler(my_gap_event_handler);


    pinMode (LED_BUILTIN,OUTPUT); //Declare the in-built LED pin as output 

}


void loop() {
  //getRssi();


  foundDevices = pBLEScan->start(3); //Scan for 3 seconds to find the Fitness band 

  //Serial.println(BLEClient::getRssi());



  while (foundDevices.getCount() >= 1)

  {

    if (Scaned_BLE_Address == My_BLE_Address && paired == false)

    {

      BLEDevice::setCustomGapHandler(my_gap_event_handler);

      Serial.println("Found Device :-)... connecting to Server as client");

       if (connectToserver(*Server_BLE_Address))

      {

      paired = true;

      Serial.println("********************LED turned ON************************");

      digitalWrite (LED_BUILTIN,HIGH);

      break;

      }

      else

      {

      Serial.println("Pairing failed");

      break;

      }

    }

    

    if (Scaned_BLE_Address == My_BLE_Address && paired == true)

    {

      Serial.println("Our device went out of range");

      paired = false;

      Serial.println("********************LED OOOFFFFF************************");

      digitalWrite (LED_BUILTIN,LOW);

      ESP.restart();

      break;

    }

    else

    {

    Serial.println("We have some other BLe device in range");

    break;

    }

  }

}

/*int BLEClient::getRssi() {
  ESP_LOGD(LOG_TAG, ">> getRssi()");
  if (!isConnected()) {
    ESP_LOGD(LOG_TAG, "<< getRssi(): Not connected");
    return 0;
  }
  // We make the API call to read the RSSI value which is an asynchronous operation.  We expect to receive
  // an ESP_GAP_BLE_READ_RSSI_COMPLETE_EVT to indicate completion.
  //
  m_semaphoreRssiCmplEvt.take("getRssi");
  esp_err_t rc = ::esp_ble_gap_read_rssi(*getPeerAddress().getNative());
  if (rc != ESP_OK) {
    ESP_LOGE(LOG_TAG, "<< getRssi: esp_ble_gap_read_rssi: rc=%d %s", rc, GeneralUtils::errorToString(rc));
    return 0;
  }
  int rssiValue = m_semaphoreRssiCmplEvt.wait("getRssi");
  ESP_LOGD(LOG_TAG, "<< getRssi(): %d", rssiValue);
  return rssiValue;
}*/
