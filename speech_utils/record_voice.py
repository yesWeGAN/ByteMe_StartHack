import pyaudio
import math
import struct
import wave
import time
import os
from utils.logger import get_logging_config
import logging.config

logging.config.dictConfig(get_logging_config())
logger = logging.getLogger(__name__)

Threshold = 40

SHORT_NORMALIZE = (1.0 / 32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2

TIMEOUT_LENGTH = 2


class Recorder:

    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        logger.debug(f'{rms * 1000} / t: {Threshold}')
        return rms * 1000

    def __init__(self, output_dir: str):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)
        self.output_dir = output_dir

    def record(self)->str:
        logger.debug('Noise detected, recording beginning')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH
        noise_detected = False

        while current <= end:
            data = self.stream.read(chunk)
            if self.rms(data) >= Threshold:
                noise_detected = True
                end = time.time() + TIMEOUT_LENGTH
            elif not noise_detected:
                # keep increasing the timer so users have more than 2 sec to start talking
                end = time.time() + TIMEOUT_LENGTH

            current = time.time()
            rec.append(data)

        return self.write(b''.join(rec))

    def write(self, recording: bytes) -> str:
        n_files = len(os.listdir(self.output_dir))

        filename = os.path.join(self.output_dir, '{}.wav'.format(n_files))

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        logger.debug(f'Wrote .wav to {filename}')
        return filename

    def listen(self):
        logger.debug('Listening beginning')
        while True:
            input = self.stream.read(chunk)
            rms_val = self.rms(input)
            if rms_val > Threshold:
                self.record()
