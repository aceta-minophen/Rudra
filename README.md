<img src="https://github.com/aceta-minophen/Rudra/blob/website/Website/public/Rudra.svg" align="right" width="200">

# Rudra
A smart healthcare assistant robot intended for home and hospital use.

## 🖲️ Human Following and Tracking
> Rudra is intended to follow the designated human around in-toe to take care of them and always be en garde for obstacles that the human might run into. This also gives Rudra the ability to assist the visually impaired and helps them navigate their surroundings safely without the need for anyone else. 

Following the human is one of the key features of Rudra and requires implementation of **Indoor Positioning System (IPS)**. While **GPS** is a sound option when walking outside, it is not possible to utilize it in the house or a hospital floor.

### Solution integration
1. **If no crowd or obstruction in robot visual range are there (<1m):** Camera used for realtime video tracking human using deep learning algorithm
2. **Indoor Positioning System:** Rudra needs to first be trained to recognize a said room using Wi-Fi RSSI values (implemented using ML; [tutorial]( https://www.hackster.io/news/indoor-positioning-using-arduino-and-machine-learning-in-4-easy-steps-295d39e5e7c9)). 
3. **In case of crowd or obstructions (<3m):** We can consider the following scenarios where Rudra loses the human:
    1. **Obstacle encountered while walking in a particular direction:** Rudra will save the direction it was previosly going at, then do the following:
        1. Turn left wrt the saved direction, go forward for 1m while looking right and turn right if obstacle passed
        2. If obstacle not passed after 1m, take clockwise 180deg turn and continue forward. Turn left if obstacle passed
        3. If obstacle not passed, repeat steps 1 and 2 for 1.5m and simultaneosly send message to phone app or bluetooth device with room location where Rudra is stuck.
        4. After obstacle has been passed, measure BLE RSSI values (and ensure that they are decreasing) to stay on the right coarse until human is spotted again.
    2. **Standing still and obstacle encountered:** Make 360deg turn and go straight as soon as obstacle ends and following the LSRB algorithm while measuring the BLE RSSI values to ensure correct path 

> Implementation here: https://github.com/aceta-minophen/Rudra/blob/tracking/Tracking/README.md

## 🏋️‍♀️ Fitness Tracking
> Rudra will be able to access data the fitness data from smartwatch and also be able to remind the human about drinking water on regular intervals (ensure that water is being drunk by logging in activity using camera). Reminders for specific medicine timings and food timings can also be set. Rudra will also be able to track the amount of calories being consumed with the specific food and compare it with the ideal amount to give suggestions on what to consume next to maintain good health.

Speech recognition and processing needs to be done for implementing this.

### Solution Integration
1. Setting up reminders for medicines and water in the app 
2. Setting up age and health specifications to allow algorithm to calculate how much water is required and at what intervals.
    1. Recording the amount of water being drunk (computer vision - noticing when human is drinking water and logging it in: **action detection**)
    2. Logging in what food is being consumed and track calories (Ex: https://play.google.com/store/apps/details?id=ai.bite.biteapp&hl=en&gl=US) 
    3. Plan next meal accordingly 
3. Fall detection using computer vision to send alert if fatal fall is detected
4. Obtaining heart rate,etc data from trackers -- _redundant and difficult to implement_

## 🗣️ Voice Assistant
> A key feature of Rudra is to be a constant companion in sickness and in health. Talking and cheering up humans is what Rudra is built for.

Smart AI is required to implement this feature so that Rudra can detect facial expressions and understand emotions, then decide what to say accordingly.

### Solution Integration
1. Ask Rudra questions (like Alexa)
2. Rudra Intents:
    1. How are you? Do you want to talk? etc
    2. Sympathetic replies to answers for the above
    3. Cracking follow up jokes or telling elaborate stories with human-like speech modulation
3. Ask Rudra to set reminders for meetings or events (like birthdays, etc)
4. Ask Rudra to make shopping lists and send said list to family member, etc.
5. Ask Rudra to send messages to or video/voice call people (integration with Rudra companion app, or maybe some other wide-use app like Whatsapp if possible)
6. Ask Rudra to send urgent alerts in case feeling unwell

## 📱 Companion App
> One app to rule them all.

Rudra Companion App will be extremely crucial in the initial setup of the robot. Then, most of the data transfer will also be accomplished using this app.

### Solution Integration
1. Remote Control
2. Setting up proximity detection and indoor positioning system
3. Configuring health settings
4. Communication features
