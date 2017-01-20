"""
Abstract interface for http services
"""
#!/usr/bin/local/python3
from abc import ABC, abstractmethod

class AbstractHttpService(ABC):
    """
    Abstract class for Microsoft Cognitive Services
    """

    @abstractmethod
    def _get_request_params(self):
        pass

    @abstractmethod
    def _translate_result(self, message, full_response=False):
        pass

    @abstractmethod
    def get_response(self, file_path, full_response=False):
        """
        Execute the request
        """
        pass

    @abstractmethod
    def get_async_response(self, file_path, response_handlers, daemon, face_rects=None):
        """
        Execute the request asyncronously
        """
        pass

    @abstractmethod
    def _async_helper_response(self, file_path, response_handlers, arg=None):
        pass

