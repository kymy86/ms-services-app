"""
Abstract the interaction with the Emotion APIs
"""
#!/usr/local/bin/python3

from urllib import parse
import json
import operator
from threading import Thread
from classes.httpservice import HttpService

class EmotionHttpService(HttpService):
    """ Abstract the interaction with the Emotion APIs"""

    _EMOTION_URI = '/emotion/v1.0/recognize'

    def __init__(self, subscription_key):
        super().__init__(subscription_key)

    def get_emotion_async(self, image_path, response_handlers, daemon, face_rects=None):
        """
        Call the emotion API in a separate thread

        Arguments:
        image_path the path of image that has to be analyzed
        response_handlers dictionary with functions to execute in async
        daemon: define if thread used for async will be daemon or not
        face_rects: if call with rectangles faces, this list contain all the rectangles
        """
        return super()._exec_async_request(
            image_path,
            response_handlers,
            self._get_emotion_async_helper,
            daemon,
            face_rects
        )

    def _get_emotion_async_helper(self, image_path, response_handlers, face_rects=None):
        """
        A wrapper function to be executed asynchronosly
        """
        res = None
        try:
            if face_rects is None:
                res = self.get_emotion(image_path)
            else:
                res = self.get_emotion_with_rect(image_path, face_rects)
        except Exception as exception:
            response_handlers['on_failure'](exception)
            return
        response_handlers['on_success'](res)


    def get_emotion(self, image_path):
        """
        Implement Emotion Recognition API:
        https://dev.projectoxford.ai/docs/services/5639d931ca73072154c1ce89/operations/563b31ea778daf121cc3a5fa

        Arguments: the image file path.
        """
        request_url = '{uri}'.format(uri=self._EMOTION_URI)
        try:
            message = super()._execute_request(image_path, request_url)
            return self._translate_result(message)
        except:
            super().logger.error('Error recognize emotion')
            raise


    def get_emotion_with_rect(self, image_path, face_rects):
        """
        Implement Emotion Recognition with Face Rectangles API:
        https://dev.projectoxford.ai/docs/services/5639d931ca73072154c1ce89/operations/56f23eb019845524ec61c4d7

        Arguments: the image file path and a list of rectangles dictionaries
        [{l:?,t:?,w:?,h:?}] with:
        l=left
        t=top
        w=width
        h=height
        """
        try:
            if len(face_rects) < 1:
                raise Exception('Error identifying image: no face rectangles provided')

            face_rects_string = ';'.join(["{0},{1},{2},{3}".format(
                r.get('l'),
                r.get('t'),
                r.get('w'),
                r.get('h')) for r in face_rects])
            request_url = '{uri}?faceRectangles={rects}'.format(
                uri=self._EMOTION_URI,
                rects=parse.quote(face_rects_string)
            )

            message = super()._execute_request(image_path, request_url)
            return self._translate_result(message)
        except:
            super().logger.error("Error recognize emotion")
            raise


    def _translate_result(self, message):
        """
        From the scores response of each image, return only the highest one
        """
        response = json.loads(message)
        return  [
            max(r['scores'].items(), key=operator.itemgetter(1))[0] for r in response
        ]
