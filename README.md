Face and Emotion detection
===========

This application contains a library and a software application for detecting user faces and emotions in real-time (near real-time)
using APIs from [Microsoft Cognitive Services][].
The library and application are implemented in Python (from version 3), and use [OpenCV] package for webcam support.

[Microsoft Cognitive Services]: https://www.microsoft.com/cognitive-services
[OpenCV]: http://opencv.org/

## Getting Started

1. Get API keys for the Emotion APIs and the Face APIs from [microsoft.com/cognitive][Sign-Up]:
    - [Emotion API][]
    - [Face API][]
2. Open the setenv_example.sh file and add the two API Keys as environment variables. Execute the script.
3. Run the client.py script

[Sign-Up]:https://www.microsoft.com/cognitive-services/en-us/sign-up
[Emotion API]: https://www.microsoft.com/cognitive-services/en-us/emotion-api
[Face API]: https://www.microsoft.com/cognitive-services/en-us/face-api

## Using the Emotion/Face libraries

You can use the two libraries with few line of code:
```
#Create the API client
emotion_client = EmotionHttpService("your_emotion_api_key")
face_client = FaceHttpService("your_face_api_key")
#Set-up the API call 
emotion = emotion_client.get_emotion("path_of_image")
face = face_client.get_face("path_of_image")
```

Both the libraries have a method for calling the API asynchronously or synchronously. See the class documentation for more
details

The Emotion API client implements the emotion recognition with Face rectangles.

