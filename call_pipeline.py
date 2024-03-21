import os

from speech_utils.record_voice import Recorder
from utils.logger import get_logging_config
from utils.audio_conversion import convert_wav_to_mp3,convert_mp3_to_wav
from speech_utils.speech_to_text import speech_to_text
from speech_utils.text_to_speech import synthesize_speech, play_audio
import logging.config

logging.config.dictConfig(get_logging_config())
logger = logging.getLogger(__name__)

logger.debug('Initalized recorder')
imput_dir = r'/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/audio'
output_dir = r'/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/audio_out'
recorder = Recorder(imput_dir)


def respond_to_caller():
    recorder.record()
    filename = os.listdir(imput_dir)[-1]
    new_file_name = convert_wav_to_mp3(os.path.join(imput_dir, filename))

    question_text = speech_to_text(new_file_name)
    print(question_text)
    # TODO all the other stuff

    response_file = synthesize_speech(question_text,output_dir)
    response_file = convert_mp3_to_wav(response_file)
    play_audio(response_file)
    return question_text
