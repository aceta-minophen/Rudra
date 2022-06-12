# Rudra - Tracking 🖲️

## 👩‍💻 Technologies Required
1. Camera - Computer Vision for detecting human and objects
2. ESP32 - Measuring Wi-Fi and BLE RSSI values
3. Phone app for training Rudra

## 🧮 Solution integration
1. **If no crowd or obstruction in robot visual range are there (<1m):** Camera used for realtime video tracking human using deep learning algorithm
2. **Indoor Positioning System:** Rudra needs to first be trained to recognize a said room using Wi-Fi RSSI values (implemented using ML; [tutorial]( https://www.hackster.io/news/indoor-positioning-using-arduino-and-machine-learning-in-4-easy-steps-295d39e5e7c9)). 
3. **In case of crowd or obstructions (<3m):** We can consider the following scenarios where Rudra loses the human:
    1. **Obstacle encountered while walking in a particular direction:** Rudra will save the direction it was previosly going at, then do the following:
        1. Turn left wrt the saved direction, go forward for 1m while looking right and turn right if obstacle passed
        2. If obstacle not passed after 1m, take clockwise 180deg turn and continue forward. Turn left if obstacle passed
        3. If obstacle not passed, repeat steps 1 and 2 for 1.5m and simultaneosly send message to phone app or bluetooth device with room location where Rudra is stuck.
        4. After obstacle has been passed, measure BLE RSSI values (and ensure that they are decreasing) to stay on the right coarse until human is spotted again.
    2. **Standing still and obstacle encountered:** Make 360deg turn and go straight as soon as obstacle ends and following the LSRB algorithm while measuring the BLE RSSI values to ensure correct path 

## Implementation
To access wearable having BLE (FitBit in our case, or earphones can even be used) and use it as a beacon and use the RSSI values to calculate distance between the tracker and Rudra.

### Pre-requisites in Rudra Configuration
1. Indoor floor plan should be available - Rudra needs to be trained first and store the locations in the system.
2. RSSI values need to be pre-configured to measure distance accurately.

### Solution Paths
1. Gain access to FitBit via the companion app https://github.com/Polidea/RxBluetoothKit/tree/master/ExampleApp
2. Using ESP32: https://community.appinventor.mit.edu/t/arduino-distance-meassuring-through-bluetooth-classic-signal-strength-rssi-project/21175/2 , https://circuitdigest.com/microcontroller-projects/esp32-ble-client-connecting-to-fitness-band-to-trigger-light, https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/BLEClient.cpp#L366-L384

1. **BLE beacons**

3. **Pairing Rudra (using bluetooth) with wearable smartwatch**
4. **Triangulating mobile hotspot signal using NodeMCU**

GPS, IPS (indoor positioning system), RTLS (real time location system)
#### Training Rudra
Setup using phone app: 
1. Move Rudra around one room to allow it to record the access points (using Wi-Fi RSSI values) and then name the room to save it in Rudra's map
2. Allow Rudra to designate key features of the room as reference flags to recognize its position in case similar RSSI values encountered in separate rooms.
3. Pair Rudra with a bluetooth wearable (watch/earphones) for Rudra to callibrate the distance with the BLE RSSI values

https://community.appinventor.mit.edu/t/arduino-distance-meassuring-through-bluetooth-classic-signal-strength-rssi-project/21175

https://www.researchgate.net/publication/322877438_Estimate_distance_measurement_using_NodeMCU_ESP8266_based_on_RSSI_technique

https://www.ijert.org/research/accurate-estimation-of-bluetooth-rssi-and-distance-IJERTV5IS030130.pdf

https://nothans.com/measure-wi-fi-signal-levels-with-the-esp8266-and-thingspeak
