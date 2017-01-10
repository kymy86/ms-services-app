"""
Abstract the interaction with the Face APIs
"""
#!/usr/bin/local/python3

from urllib import parse
import json
from classes.httpservice import HttpService

class FaceHttpService(HttpService):
    """ Abstract the interaction with the Face APIs"""

    _FACE_URI = '/face/v1.0/detect'

    def __init__(self, subscription_key):
        super().__init__(subscription_key)

    def _get_request_params(self):
        return parse.urlencode({
            'returnFaceId' : 'true',
            'returnFaceLandmarks' : 'false',
            'returnFaceAttributes' : 'age,gender'
        })

    def get_face(self, image_path, full_response=False):
        """
        Implement the Face Recognition API (Detect)
        https://dev.projectoxford.ai/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395236
        Arguments: the image file path.
        full_response if you want to get the full not parsed response, put this flag to True
        """
        request_url = '{uri}?{params}'.format(
            uri=self._FACE_URI,
            params=self._get_request_params()
            )
        try:
            message = super()._execute_request(image_path, request_url)
            return self._translate_result(message, full_response)
        except:
            super().logger.error('Error recognize emotion')
            raise

    def get_face_async(self, image_path, response_handlers, daemon):
        """
        Call the face API in a separate thread

        Arguments:
        image_path the path of image that has to be analyzed
        response_handlers dictionary with functions to execute in async
        daemon: define if thread used for async will be daemon or not
        face_rects: if call with rectangles faces, this list contain all the rectangles
        """
        return super()._exec_async_request(
            image_path,
            response_handlers,
            self._get_face_async_helper,
            daemon)

    def _get_face_async_helper(self, image_path, response_handlers, face_rects=None):
        """
        A wrapper function to be executed asynchronosly
        """
        res = None
        try:
            res = self.get_face(image_path)
        except Exception as exception:
            response_handlers['on_failure'](exception)
            return
        response_handlers['on_success'](res)

    def _translate_result(self, message, full_response=False):
        """
        From the response return only the age and gender attributes

        Arguments:
        full_response if you want to get the full not parsed response, put this flag to True
        """
        response = json.loads(message)
        if full_response:
            return response
        else:
            return  [
                r['faceAttributes'] for r in response
            ]


