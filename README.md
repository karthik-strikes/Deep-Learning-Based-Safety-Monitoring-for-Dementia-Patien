# Deep Learning-Based Safety Monitoring for Dementia Patients

## Description

Dementia, particularly Alzheimer's disease, is increasingly prevalent among the elderly. Monitoring and caring for individuals affected by this condition is paramount. This project introduces an innovative approach to Human Activity Recognition (HAR), essential for observing elderly and coma patients in unsupervised settings. Utilizing skeletal joint kinematics, our method intelligently recognizes human actions, offering both high accuracy and cost-effectiveness. An independent smartphone application complements this system, monitoring patients’ conditions and surroundings, and featuring a Notification API for urgent alerts.

This initiative serves as a proof of concept for a method aiding elderly citizens and children in emergencies or health crises.

## Objectives
* Utilize human skeletal joint positions for accurate Human Activity Recognition.
* Develop an intelligent system for recognizing human actions and gestures from live images or videos, and create models to identify abnormal activities.
* Collect and train datasets on different skeletal images of human actions using deep learning algorithms.
* Implement a React Native application for live streaming, enabling the detection of abnormal activities at home.
* Send alert notifications through the mobile app when abnormal activities are detected.

## Dependencies
```plaintext
pip install flask==1.1.1
pip install sklearn==0.23.2
pip install tensorflow==2.3.1
pip install tinydb==3.15.2
pip install face_recognition
pip install imutils
pip install opencv==4.2.0
pip install socket
pip install numpy==1.18.5
pip install flask
pip install requests
pip install threading
pip install json
```

## Executing Program
```bash
python main.py --ip 0.0.0.0 --port 8000
```

## System Architecture

[![System Architecture](https://user-images.githubusercontent.com/91920989/186725773-841a7aa5-f099-49be-8c98-309df374e18e.png)](#)  
*Figure 1: Overview of the System Architecture*

## Modules

### Human Activity Collection
We capture live data of standard human poses (fall, sleep, sit, stand) and store them in separate folders. Our deep learning approach to action recognition aims for unique outcomes beyond traditional methods.

### Labelling of Dataset
Data labelling, critical for accuracy in machine learning, involves tagging each input with poses for frame-specific identification. This ensures the trained model's precision.

![Data Labelling Example](https://user-images.githubusercontent.com/91920989/186427520-6dc6367d-e4f5-49f2-8fa1-7140e298a09a.png)  
*Figure 2: Example of Data Labelling in the Dataset*

### Developing a Model File
We use a sequential CNN network algorithm for training our human activity dataset, offering simplicity and high accuracy. The model layers are interconnected, utilizing dense layers for effective data processing.

### Live Streaming
Leveraging IoT for real-time data transmission, we stream live video and audio to the user, showcasing our system's capability in monitoring and recognition.

![Live Streaming Interface](https://user-images.githubusercontent.com/91920989/186436325-1f23e452-e059-4d15-b004-f52a6a430e4f.jpg)  
*Figure 3: Live Streaming Interface*

### React Native Application
The mobile app, developed using React Native, acts as an accessible user interface. It alerts users to abnormal activities detected during live streaming.

![React Native App Interface](https://user-images.githubusercontent.com/91920989/186730336-332f195d-568e-404a-92e8-86b714c083a3.jpg)  
*Figure 4: Mobile Application Interface for Alerts*

## Advantages of the Proposed System
* Enhanced accuracy with advanced algorithms.
* Increased safety for the elderly and children.
* Real-time monitoring via a dedicated mobile application.
* Potential to save lives through prompt detection and response.
