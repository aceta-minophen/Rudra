# Rudra - Companion App 📱

> One app to rule them all.

Rudra Companion App will be extremely crucial in the initial setup of the robot. Then, most of the data transfer will also be accomplished using this app.

## Technologies Required
1. Flutter
2. AWS 
3. Firebase 

## Solution Integration
1. Remote Control - [Joystick app](https://medium.com/@gilesjeremydev/create-a-virtual-joystick-for-flame-game-cf62cad7bc4)
2. Setting up proximity detection and indoor positioning system
3. Configuring health settings
4. Communication features
5. Reminders and calendar

## App Architecture
5 tabs at the bottom for remote control, settings, chat/call, health, reminders+calendar
### UI
1. Settings
    1. Configuration for pairing Rudra with Bluetooth wearable (earphone/smartwatch)
    2. Health configurations for age, weight, height and gender
    3. Account info and details about relationship with Rudra owner (family member/medical official, along with control permisions for each account): if remote control not permissed, then not visible, etc.
2. Remote Control - Landscape orientation
    1. Full page camera live feed (like vid games) including audio
    2. Joystick controls in rightmost and leftmost corners (righmost for direction control, leftmost for speed control); data values visible above the control knobs
    3. Name of the room (editable) visible on bottom centre & Configuration for indoor positioning system (Wi-Fi RSSI values alongside room name)
    4. Live object and obstacle recognition visible with markings for estimated aspect ratio, distance and label (editable label)
    5. Flag marking option for training Rudra in recognizing room in case RSSI values glitch
    6. Mute/unmute button on topright corner to talk remotely
3. Chat/call
    1. Individual/group texting or calling (like whatsapp)
    2. Only video output option available but not input (can see Rudra video feed but cannot turn on your own camera)
4. Health
    1. Daily/weekly/monthly water log/reminder [square icon]
    2. Daily (3/4 times) food log: food name [scrollable menu]
    3. Calory log (graphed, against average ideal amount required at the age)
    4. Recommedation for next meal according to previous data
    5. Medicine reminder (if any) - editable
5. Reminders/Calendar
    1. Simple calendar with upcoming events, etc (can be integrated with google calendar)
