
#!/usr/local/bin/python3

import os
from pathlib import Path
from classes.webcamclient import WebcamClient
from classes.audioclient import AudioClient


def on_success(res):
    """print thread success result"""
    print(res)

def on_failure(res):
    """ print thread failure result"""
    print(res)

HANDLERS = {'on_success':on_success, 'on_failure': on_failure}

def main(user_input):
    """ execute the ms emotion apis """
    try:
        client = WebcamClient(os.environ['EMOTION_API'], os.environ['FACE_API'], HANDLERS)
        user_input = "1" if user_input == 'emotion' else "2"
        client.run(user_input)
    except KeyboardInterrupt:
        temp_image = Path(client.IMAGE_PATH)
        if temp_image.is_file():
            os.remove(client.IMAGE_PATH)
        exit(0)

if __name__ == '__main__':

    print("Say 'Emotion' if you want to detect the emotion")
    print("Say 'Face' if you want to detect the face")

    user_input = ""
    audioclient = AudioClient(os.environ['SPEECH_API'])
    while user_input not in ["emotion", "face"]:
        print("I'm listening.... ")
        user_input = audioclient.run().lower()
        print("You're wrong: You said: {}".format("unrecognizable word" if user_input == 'error' else user_input))
    main(user_input)
