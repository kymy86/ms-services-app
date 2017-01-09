
#!/usr/local/bin/python3

import os
from pathlib import Path
from classes.webcamclient import WebcamClient


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
        client.run(user_input)
    except KeyboardInterrupt:
        temp_image = Path(client.IMAGE_PATH)
        if temp_image.is_file:
            os.remove(client.IMAGE_PATH)
        exit(0)

if __name__ == '__main__':
    print("Press 1 if you want detect the emotion")
    print("Press 2 if you want detect the face")
    user_input = ""
    while user_input not in ["1", "2"]:
        user_input = input("Make your choice (1/2): ")
    main(user_input)
