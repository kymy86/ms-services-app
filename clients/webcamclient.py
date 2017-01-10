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
from classes.computervisionhttpservice import ComputerVisionService


class WebcamClient():
    """
    Wrapper for opencv detection software
    """
    logger = logging.getLogger('webcam_client')
    IMAGE_PATH = 'images/frame.jpg'
    _CASCADE_CLASSIFIER = 'data/haarcascade_frontalface_alt2.xml'
    _local_face = True
    _user_choices = {}
    _is_emotion = False
    _is_face = False
    _is_cv = False

    def __init__(self, emotion_api, face_api, computer_vision_api, handlers):
        self.emotion_client = EmotionHttpService(emotion_api)
        self.face_client = FaceHttpService(face_api)
        self.cv_client = ComputerVisionService(computer_vision_api)
        self.handlers = handlers
        self.face_cascade = cv2.CascadeClassifier(self._CASCADE_CLASSIFIER)
        self._set_logger()

    def disable_local_faces(self):
        """ Disable OpenCV local face recognition"""
        self._local_face = False

    def enable_local_faces(self):
        """ Enable OpenCV local face recognition"""
        self._local_face = True

    def set_emotion(self):
        """ Enable the emotion detection"""
        self._is_emotion = True

    def set_face(self):
        """ Enable the face detection """
        self._is_face = True

    def set_cv(self):
        """ Enable the computer vision algorithm"""
        self._is_cv = True

    def _detect_local_faces(self):
        """
        Run detection of faces by using opencv detection
        algorithm
        """
        rects = []
        if not self._local_face:
            return [None], None

        image_temp = cv2.imread(self.IMAGE_PATH)
        gray = cv2.cvtColor(image_temp, cv2.COLOR_BGR2GRAY)
        self.logger.info("Local faces detection...")
        faces = self.face_cascade.detectMultiScale(
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
        self.logger.info("Found {} local faces".format(len(faces)))
        return faces, rects

    def run(self):
        """
        Run the face/emotion/computer-vision detection by calling the Microsft Cognitive Services
        """
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            self.logger.error("No webcam Available")
            exit(0)

        while True:
            sleep(3)
            self.logger.info("Grabbing Frame")
            ret, frame = video_capture.read()
            cv2.imwrite(self.IMAGE_PATH, frame)

            faces, rects = self._detect_local_faces()

            if self._is_emotion:
                if len(faces) != 0:
                    self.emotion_client.get_emotion_async(
                        self.IMAGE_PATH,
                        self.handlers,
                        False,
                        rects)
            elif self._is_face:
                if len(faces) != 0:
                    self.face_client.get_face_async(
                        self.IMAGE_PATH,
                        self.handlers,
                        False)
            else:
                self.cv_client.get_computer_vision_async(
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


