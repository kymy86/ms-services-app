"""
Run the ms speech recognition API detecting speech from
notebook microphone (pyaudio)
https://people.csail.mit.edu/hubert/pyaudio/
"""
#!/usr/local/bin/python3

import logging
import wave
import pyaudio
from classes.speechttpservice import SpeechHttpService

class AudioClient():
    """
    Wrapper for pyaudio detection software
    """
    logger = logging.getLogger('audio_client')
    AUDIO_PATH = 'audio/track.wav'
    _FORMAT = pyaudio.paInt16
    _CHANNELS = 2
    _RATE = 44100
    _CHUNK = 1024
    _records_seconds = 0

    def __init__(self, speech_api, seconds=5, handlers=None):
        self.speech_client = SpeechHttpService(speech_api)
        self._records_seconds = seconds
        self.handlers = handlers
        self._set_logger()

    def _record_audio(self, frames, audio):
        """ Record the audio in a wav file"""
        with wave.open(self.AUDIO_PATH, 'wb') as waveFile:
            waveFile.setnchannels(self._CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(self._FORMAT))
            waveFile.setframerate(self._RATE)
            waveFile.writeframes(b''.join(frames))

    def run(self):
        """ Listen the microphone and call the MS API"""
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=self._FORMAT,
            channels=self._CHANNELS,
            rate=self._RATE,
            input=True,
            frames_per_buffer=self._CHUNK)
        frames = []

        for i in range(0, int(self._RATE/self._CHUNK*self._records_seconds)):
            data = stream.read(self._CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()
        self._record_audio(frames, audio)
        return self.speech_client.get_speech(self.AUDIO_PATH)


    def _set_logger(self):
        """ Set the logger for the http client """
        self.logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
