import os
import re

from speech_utils.record_voice import Recorder
from utils.logger import get_logging_config
from utils.audio_conversion import convert_wav_to_mp3, convert_mp3_to_wav
from openai_interface import call_endpoints
from speech_utils.text_to_speech import play_audio
from speech_utils.speech_to_text import record_and_transcribe
from utils.audio_conversion import convert_mp3_to_wav
import logging.config

logging.config.dictConfig(get_logging_config())
logger = logging.getLogger(__name__)

logger.debug('Initalized recorder')
input_dir = r'/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/audio'
output_dir = r'/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/audio_out'
recorder = Recorder(input_dir)


def respond_to_caller():
    # greet the user with a prerecorded message

    #play_audio(r'/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/speech_utils/St_gallen_welcome.wav')
    #caller_response = record_and_transcribe(recorder=recorder)
#
#
    ## TODO all the other stuff
#
    ## Convert the chatbots answer back to voice
    #response_file = call_endpoints.convert_answer_to_audio(caller_response, output_dir)
    #response_file_wav = convert_mp3_to_wav(response_file)
    #logger.debug('Stored response in {response_file_wav}')
    #play_audio(response_file_wav)
#
    #play_audio(r'/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/speech_utils/satisfaction_inquiry.wav')

    satisfaction_respone = record_and_transcribe(recorder=recorder)

    see_human = call_endpoints.check_satisfaction(satisfaction_respone)
    logger.debug(f'Should we connect to a human:{see_human}')

    pattern_yes = re.compile('.*ja.*',re.IGNORECASE)
    if re.search(pattern_yes,see_human):
        logger.debug('Forwarding client')
        pass
    else:
        logger.debug('Terminating Call')

