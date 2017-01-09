"""
Run the ms emotion APIs detecting faces by using the
notebook webcam (opencv library)
http://opencv.org/
"""
#!/usr/local/bin/python3

import logging
from time import sleep
import cv2
from classes.emotionhttpservice import EmotionHttpService
from classes.facehttpservice import FaceHttpService


class WebcamClient():
    """
    Wrapper for opencv detection software
    """
    logger = logging.getLogger('webcam_client')
    IMAGE_PATH = 'images/frame.jpg'
    _CASCADE_CLASSIFIER = 'data/haarcascade_frontalface_alt2.xml'

    def __init__(self, emotion_api, face_api, handlers):
        self.emotion_client = EmotionHttpService(emotion_api)
        self.face_client = FaceHttpService(face_api)
        self.handlers = handlers
        self._set_logger()

    def _detect_local_faces(self):
        """
        Run detection of faces by using opencv detection
        algorithm
        """
        face_cascade = cv2.CascadeClassifier(self._CASCADE_CLASSIFIER)
        rects = []
        image_temp = cv2.imread(self.IMAGE_PATH)
        gray = cv2.cvtColor(image_temp, cv2.COLOR_BGR2GRAY)
        logging.info("Local faces detection...")
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        for (length, top, width, height) in faces:
            rects.append({
                'l':length,
                't':top,
                'w':width,
                'h':height
            })
        return faces, rects

    def run(self, user_choice):
        """
        Run the face/emotion detection by calling the Microsft Cognitive Services
        Arguments:
        user_choice: if "1", user decided to detect the emotion
        if "2", user deceided to detect the face
        """
        video_capture = cv2.VideoCapture(0)
        while True:
            sleep(3)
            self.logger.info("Grabbing Frame")
            ret, frame = video_capture.read()
            cv2.imwrite(self.IMAGE_PATH, frame)

            faces, rects = self._detect_local_faces()
            self.logger.info("Found {} local faces".format(len(faces)))

            if len(faces) != 0:
                if user_choice == "1":
                    self.emotion_client.get_emotion_async(
                        self.IMAGE_PATH,
                        self.handlers,
                        False,
                        rects)
                else:
                    self.face_client.get_face_async(
                        self.IMAGE_PATH,
                        self.handlers,
                        False
                    )
        video_capture.release()

    def _set_logger(self):
        """ Set the logger for the http client """
        self.logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)


