"""
This class implement the http module that allow the interaction
with the Microsoft Cognitive services APIs
"""
#!/usr/bin/local/python3

import logging
from http import client
from threading import Thread
from contextlib import closing

class HttpService():
    """ Abstract the interaction with the Microsoft APIs"""

    _BASE_URI = 'api.projectoxford.ai'
    _SUBSCRIPTION_KEY_HEADER = 'Ocp-Apim-Subscription-Key'
    _CONTENT_TYPE_HEADER = 'Content-Type'
    _JSON_CONTENT_HEADER = 'application/json'
    _STREAM_CONTENT_HEADER = 'application/octet-stream'
    _STATUS_OK = 200
    _LOG_PATH = 'logs/httpservice.log'
    logger = logging.getLogger('http_client')

    def __init__(self, subscription_key):
        self._subscription_key = subscription_key
        self._set_logger()

    def _set_logger(self):
        """ Set the logger for the http client """
        self.logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(self._LOG_PATH)
        file_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(module)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def _execute_request(self, image_path, request_url):
        """
        Execute the request

        Arguments:
        image_path the path of image that has to be analyzed
        request_url the url of the API to be called
        """
        try:
            with open(image_path, 'rb') as body:
                res, message = self._send_request(
                    'POST',
                    self._BASE_URI,
                    request_url,
                    self._STREAM_CONTENT_HEADER,
                    body)
            if res.status == self._STATUS_OK:
                return message
            else:
                reason = res.reason if not message else message
                raise Exception('Recognize error: '+reason)
        except:
            self.logger.error('Recognize error')
            raise

    def _exec_async_request(self, image_path, response_handlers, helper_func, daemon, face_rects=None):
        """
        Call the API in a separate thread

        Arguments:
        image_path the path of image that has to be analyzed
        response_handlers dictionary with functions to execute in async
        helper_func the wrapper function to be executed asynchronosly
        daemon: define if thread used for async will be daemon or not
        face_rects: if call with rectangles faces, this list contain all the rectangles
        """
        if 'on_success' not in response_handlers:
            raise KeyError('You have to specify the success handler with key "on_success"')
        if 'on_failure' not in response_handlers:
            raise KeyError('You have to specify the failure handler with key "on_failure"')

        emotion_thread = Thread(
            target=helper_func,
            args=(image_path, response_handlers, face_rects))
        emotion_thread.daemon = daemon
        emotion_thread.start()
        return emotion_thread


    def _send_request(self, method, base_url, request_url, content_type=None, body=None, headers=None):
        """
        Perform the HTTP request.
        Arguments:
        method = HTTP method
        base_url = HTTP base url
        request_url = the request url for the connection
        content_type = The value of content type in the header
        body = the body of the request (need only for POST requests)
        headers = the headers of the request if it requires custom headers
        """
        try:
            if headers is None:
                headers = {
                    self._CONTENT_TYPE_HEADER:content_type,
                    self._SUBSCRIPTION_KEY_HEADER:self._subscription_key
                }

            with closing(client.HTTPSConnection(base_url)) as conn:
                conn.request(method, request_url, body, headers)
                res = conn.getresponse()
                message = res.read().decode('utf-8')
                return res, message
        except:
            self.logger.error("Error sending request")
            raise
