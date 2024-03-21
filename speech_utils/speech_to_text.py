import logging.config
import os

from speech_utils.record_voice import Recorder
from openai_interface import call_endpoints
from utils.audio_conversion import convert_wav_to_mp3
from utils.logger import get_logging_config

logging.config.dictConfig(get_logging_config())
logger = logging.getLogger(__name__)


def record_and_transcribe(recorder: Recorder) -> str:
    # record the inital user request

    filename = recorder.record()
    new_file_name = convert_wav_to_mp3(filename)
    logger.debug(f'Stored user request in {new_file_name}')

    # convert the users voice to text
    transcribed_text = call_endpoints.convert_question_to_text(new_file_name)
    logger.debug(f'User: {transcribed_text}')

    return transcribed_text
