from pydub import AudioSegment

from utils.logger import get_logging_config
import logging.config

logging.config.dictConfig(get_logging_config())
logger = logging.getLogger(__name__)
def convert_wav_to_mp3(file_name):
    logger.debug(f'Converting audio in {file_name} to mp3')
    audio = AudioSegment.from_wav(file_name)
    new_file_name = f"{file_name.rstrip('.wav')}.mp3"
    audio.export(new_file_name, format="mp3")

    return new_file_name

def convert_mp3_to_wav(file_name):
    logger.debug(f'Converting audio in {file_name} to wav')
    audio = AudioSegment.from_mp3(file_name)
    new_file_name = f"{file_name.rstrip('.mp3')}_output.wav"
    audio.export(new_file_name, format="wav")

    return new_file_name
