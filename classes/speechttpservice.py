"""
Abstract the interaction with the Bing Speech API
"""
#!/usr/local/bin/python3

from urllib import parse
import json
import uuid
from classes.httpservice import HttpService
from classes.abstracthttpservice import AbstractHttpService

class SpeechHttpService(HttpService, AbstractHttpService):
    """ Abstract the interaction with the Bing Speech API"""

    _SPEECH_URI = '/recognize'
    _BASE_URI = 'speech.platform.bing.com'
    _AUTH_BASE_URI = 'api.cognitive.microsoft.com'
    _AUTH_API_URI = '/sts/v1.0/issueToken'
    _AUTH_HEADER = 'Authorization'

    _token = None
    _locale = None
    _device_os = None

    def __init__(self, subscription_key, locale='en-US', device_os='MACOSX'):
        super().__init__(subscription_key)
        self._set_token()
        self._locale = locale
        self._device_os = device_os

    def _set_token(self):
        """Call the Microsoft Service to get the Authentication Token"""

        headers = {
            super()._SUBSCRIPTION_KEY_HEADER:self._subscription_key
        }
        try:
            res, token = super()._send_request(
                'POST',
                self._AUTH_BASE_URI,
                self._AUTH_API_URI,
                None,
                None,
                headers
                )
            if res.status == super()._STATUS_OK:
                self._token = token
            else:
                reason = res.reason if not token else token
                raise Exception("Auth Error "+reason)
        except:
            super().logger.error("Auth Error")
            raise

    def _execute_speech_request(self, audio_path, request_url):
        """
        Execute the HTTP request by passing the JWT
        Arguments:
        audio_path: the path of the audio file
        request_url: the url of the request
        """

        headers = {
            self._AUTH_HEADER:'Bearer '+self._token
        }
        try:
            with open(audio_path, 'rb') as body:
                res, message = super()._send_request(
                    'POST',
                    self._BASE_URI,
                    request_url,
                    None,
                    body,
                    headers)
            if res.status == self._STATUS_OK:
                return message
            else:
                reason = res.reason if not message else message
                raise Exception('Recognize error: '+reason)
        except:
            self.logger.error('Recognize error')
            raise

    def _get_request_params(self):
        """ Define the HTTP request params """
        return parse.urlencode({
            'Version' : '3.0',
            'requestid' : uuid.uuid4(),
            'appID' : 'D4D52672-91D7-4C74-8AD8-42B1D98141A5',
            'format' : 'json',
            'locale' : self._locale,
            'device.os' : self._device_os,
            'scenarios' : 'ulm',
            'instanceid' : uuid.uuid4()
        })

    def get_response(self, audio_path, full_response=False):
        """
        Implement the Bing Voice Recognition
        https://www.microsoft.com/cognitive-services/en-us/Speech-api/documentation/API-Reference-REST/BingVoiceRecognition
        Arguments: the audio file path.
        """

        request_url = '{uri}?{params}'.format(
            uri=self._SPEECH_URI,
            params=self._get_request_params())
        try:
            message = self._execute_speech_request(audio_path, request_url)
            return self._translate_result(message, full_response)
        except:
            super().logger.error('Error recognize speech')
            raise

    def get_async_response(self, audio_path, response_handlers, daemon):
        """
        Call the speech recognition API in a separate thread

        Arguments:
        image_path the path of image that has to be analyzed
        response_handlers dictionary with functions to execute in async
        daemon: define if thread used for async will be daemon or not
        face_rects: if call with rectangles faces, this list contain all the rectangles
        """
        return super()._exec_async_request(
            audio_path,
            response_handlers,
            self._async_helper_response,
            daemon
        )

    def _async_helper_response(self, audio_path, response_handlers, arg=None):
        """
        A wrapper function to be executed asynchronosly
        """
        res = None
        try:
            res = self.get_response(audio_path)
        except Exception as exception:
            response_handlers['on_failure'](exception)
            return
        response_handlers['on_success'](res)

    def _translate_result(self, message, full_response=False):
        """
        From the response return only the recognized word

        Arguments:
        full_response if you want to get the full not parsed response, put this flag to True
        """
        response = json.loads(message)
        if full_response:
            return response
        else:
            if response['header']['status'] == 'error':
                return "Error"
            else:
                return response['results'][0]['lexical']

