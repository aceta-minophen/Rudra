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
> Rudra is intended to follow the designated human around in-toe to take care of them and always be en garde for obstacles that the human might run into. This also gives Rudra the ability to assist the visually impaired and help them navigate their surroundings safely without the need for anyone else's help. 

Following the human is one of the key features of Rudra and requires implementation of **Indoor Positioning System (IPS)**. While **GPS** is a sound option when walking outside, it is not possible to utilize it in the house or a hospital floor.

#### Problem
To access fitness tracker (FitBit in our case) and use it as a BLE beacon.

1. **BLE beacons**

3. **Pairing Rudra (using bluetooth) with wearable smartwatch**
4. **Triangulating mobile hotspot signal using NodeMCU**

GPS, IPS (indoor positioning system), RTLS (real time location system)
#### TODO
