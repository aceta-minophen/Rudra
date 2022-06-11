<img src="https://github.com/aceta-minophen/Rudra/blob/website/Website/public/Rudra.svg" align="right" width="200">

# Rudra
A smart healthcare assistant robot intended for home and hospital use. 

## Features of Rudra

- Human following (small range and wide range)
  - Indoor Mapping (very important)
  - Tracking using bluetooth RSSI values from phone + close range computer vision OR
  - Tracking using triangulation by NodeMCU wifi modules OR
  - Tracking using BLE in wearables
- Fitness tracking with compatibility to existing wearables
  - Obtaining data directly from the tracker 
  - Obtaining data from tracker companion app using 3rd party
- Voice Assistant
  - Scheduling
  - Reminders (for food, water, medicines, etc.)
  - Friendly chatting features
- Computer Vision
  - Face recognition
  - Obstacle detection with warning system for the visually impaired
  - Age detection + distinguishing abilities for different people
  - Proximity detection for precisely following the assigned person
- Remote Control
  - Remote camera access for relatives and medical professionals if needed
  - Remote control for Rudra in app 
  - Calling features in case of want or emergencies

### Human Following and Tracking
> Rudra is intended to follow the designated human around in-toe to take care of them and always be en garde for obstacles that the human might run into. This also gives Rudra the ability to assist the visually impaired and helps them navigate their surroundings safely without the need for anyone else. 

Following the human is one of the key features of Rudra and requires implementation of **Indoor Positioning System (IPS)**. While **GPS** is a sound option when walking outside, it is not possible to utilize it in the house or a hospital floor.

#### Solution integration
1. **If no crowd or obstruction in robot visual range are there (<1m):** Camera used for realtime video tracking human using deep learning algorithm
2. **Indoor Positioning System:** Rudra needs to first be trained to recognize a said room using Wi-Fi RSSI values (implemented using ML; [tutorial]( https://www.hackster.io/news/indoor-positioning-using-arduino-and-machine-learning-in-4-easy-steps-295d39e5e7c9)). 
3. **In case of crowd or obstructions (<3m):** We can consider the following scenarios where Rudra loses the human:
    1. **Obstacle encountered while walking in a particular direction:** Rudra will save the direction it was previosly going at, then do the following:
        1. Turn left wrt the saved direction, go forward for 1m while looking right and turn right if obstacle passed
        2. If obstacle not passed after 1m, take clockwise 180deg turn and continue forward. Turn left if obstacle passed
        3. If obstacle not passed, repeat steps 1 and 2 for 1.5m and simultaneosly send message to phone app or bluetooth device with room location where Rudra is stuck.
        4. After obstacle has been passed, measure BLE RSSI values (and ensure that they are decreasing) to stay on the right coarse until human is spotted again.
    2. **Standing still and obstacle encountered:** Make 360deg turn and go straight as soon as obstacle ends and following the LSRB algorithm while measuring the BLE RSSI values to ensure correct path 

#### Problem
To access wearable having BLE (FitBit in our case, or earphones can even be used) and use it as a beacon and use the RSSI values to calculate distance between the tracker and Rudra.

#### Solution Paths
1. Gain access to FitBit via the companion app https://github.com/Polidea/RxBluetoothKit/tree/master/ExampleApp
2. Using ESP32: https://community.appinventor.mit.edu/t/arduino-distance-meassuring-through-bluetooth-classic-signal-strength-rssi-project/21175/2 , https://circuitdigest.com/microcontroller-projects/esp32-ble-client-connecting-to-fitness-band-to-trigger-light, https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/BLEClient.cpp#L366-L384

1. **BLE beacons**

3. **Pairing Rudra (using bluetooth) with wearable smartwatch**
4. **Triangulating mobile hotspot signal using NodeMCU**

GPS, IPS (indoor positioning system), RTLS (real time location system)
#### TODO
