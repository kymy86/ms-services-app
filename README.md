Python app wiht Microsoft Cognitive Service
===========

This software detects user faces, emotions and speech in real-time (near real-time)
using APIs from [Microsoft Cognitive Services][].
The application is implemented in Python (from version 3.5), and use [OpenCV] package for webcam support and [PyAudio] for microphone support.

[Microsoft Cognitive Services]: https://www.microsoft.com/cognitive-services
[OpenCV]: http://opencv.org/
[PyAudio]: https://people.csail.mit.edu/hubert/pyaudio/

## Getting Started

1. Get API keys for the Emotion APIs and the Face APIs from [microsoft.com/cognitive][Sign-Up]:
    - [Emotion API][]
    - [Face API][]
    - [Speech API][]
    - [Computer Vision API][]
2. Open the setenv_example.sh file and add the three API Keys as environment variables. Execute the script.
3. Run the client.py script