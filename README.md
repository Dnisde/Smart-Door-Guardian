# EC544-SmartDoorBell-Final-Project

## Introduction

In this project, we plan to build a smart door guardian system that allows the user to enter  the home without bringing the key. In the meantime, the system is mainly designed by enhancing the security of the home and integrating techniques of the networking and physical world between devices and devices. The smart guardian system uses real-time face recognition as a primary option, that identifies whether the person is the host or not. The system also supports the recognition of the voice by asking user to provide voice password through a microphone.

## System Workflow

Voice input and conduct certain actions such as informing the host or opening the door. Specifically, it will follow the instructions as shown.
One-click start: Users can decide one of the two measures to check its identity, either by face recognition or voice password, by single or double clicking the IoT button.
- Real-time face recognition: Recognize the incoming person’s identity by face recognition. Triggered by single-clicking the IoT button, the program will start running real-time face recognition and open the door if the person is the real host.
- Voice password recognition: Triggered by double-clicking the IoT button. The program will recognize the incoming person’s identity by checking if the person has given the pre-set voice password.

The door system has the following states: Non-Start, Sleep and Alert. When Sleep, it does nothing until someone presses the IoT button to save power. In alert state, it will immediately inform the host to check the camera until the host deactivates the alert signal. The workflow of the door system is shown below.


![workflow](https://github.com/Dnisde/EC544_Smart-Door-Guardian/blob/main/Workflow.png?raw=true)

