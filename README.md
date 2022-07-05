# EC544-SmartDoorGuardian-Final-Project

## Introduction

In this project, we designed and created a smart door guardian system that allows users to enter their homes without bringing a key. In the meantime, the system is mainly designed by enhancing the security of the home and implementing networking between devices. The smart guardian system uses real-time face recognition as a primary option, that identifies the incoming person's identity. The system also supports the recognition of the voice by asking the user to provide a voice password through a microphone to verify the identity. We used AWS's MQTT client as the primary communication channel between the modules in this project.

## System Workflow

The system can receive facial/voice input and conduct certain actions such as informing the host or opening the door. Specifically, it will follow the instructions as shown.
- One-click door opening: Users can decide on one of the two measures to check their identity, either by face recognition or voice password, by single or double-clicking the IoT button. The door will open right after once verified the user's identity.
- Real-time face recognition: Recognize the incoming person’s identity by face recognition. Triggered by single-clicking the IoT button, the program will start running real-time face recognition and open the door if the person is the real host.
- Voice password recognition: Triggered by double-clicking the IoT button. The program will recognize the incoming person’s identity by checking if the person has given the pre-set voice password.

The door system has the following states: Non-Start, Sleep, and Alert. When Sleeping, it does nothing until someone presses the IoT button to save power. In an alert state, it will immediately inform the host to check the camera until the host deactivates the alert signal. The workflow of the door system is shown in the figure below.

![workflow](https://github.com/Dnisde/EC544_Smart-Door-Guardian/blob/main/Workflow.png?raw=true)

## Network Architecture

Integration of the modules involved in this project, the AWS IoT button, the central computing module, and the door module are shown in the figure below. Face recognition and voice recognition modules are implemented on the Raspberry Pi 4. The communication between the AWS IoT button, the central computing module, and the door module is accomplished over the AWS MQTT topic.

![NetworkArchitecture](https://github.com/Dnisde/EC544_Smart-Door-Guardian/blob/main/Network%20Architecture.png?raw=true)
