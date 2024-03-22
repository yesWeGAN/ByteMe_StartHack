import logging.config
import re
import time

from openai_interface import call_endpoints
from speech_utils.record_voice import Recorder
from speech_utils.speech_to_text import record_and_transcribe
from utils.audio_conversion import convert_mp3_to_wav, play_audio
from utils.logger import get_logging_config
from utils.hit_filtering import filter_hits_threshold,create_summary_str,restructure_contact_urls
from vector_store.inference import KNNSimpleInference, KNNIndexInference

logging.config.dictConfig(get_logging_config())
logger = logging.getLogger(__name__)

logger.debug('Initalized recorder')
input_dir = r'/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/audio'
output_dir = r'/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/audio_out'
recorder = Recorder(input_dir)

raw_data_path = "/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/src/cpl"
indexInf = KNNIndexInference(dataset="/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/src/cpl",
                             outputpath="src/index_files")

def respond_to_caller():
    # greet the user with a prerecorded message
    play_audio(r'/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/src/St_gallen_welcome.wav')
    caller_response = record_and_transcribe(recorder=recorder)

    # sort search results
    answers, questions, dists = indexInf.run_inference(query=caller_response, k=5, printprop=False)
    answers,questions = filter_hits_threshold(answers=answers,questions=questions)
    summary_str = create_summary_str(answers=answers,questions=questions,original_question=caller_response)
    logger.debug(summary_str)
    ai_summary = call_endpoints.summarize_search(summary_str)
    logger.debug(f'ChatGPT summmary: {ai_summary}')

    pattern = re.compile("kein", re.IGNORECASE)
    if re.search(pattern,ai_summary):
        filtered_identifiers = restructure_contact_urls(faiss_seperator='_',contact_dict_seperator='/',filenames=questions)

        return

    # Convert the chatbots answer back to voice
    response_file = call_endpoints.convert_answer_to_audio(ai_summary, output_dir)
    response_file_wav = convert_mp3_to_wav(response_file)
    logger.debug('Stored response in {response_file_wav}')
    play_audio(response_file_wav)

    time.sleep(1)

    play_audio(r'/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/src/satisfaction_inquiry.wav')
    satisfaction_respone = record_and_transcribe(recorder=recorder)

    see_human = call_endpoints.check_satisfaction(satisfaction_respone)
    logger.debug(f'Should we connect to a human:{see_human}')

    pattern_yes = re.compile('.*ja.*', re.IGNORECASE)
    if re.search(pattern_yes, see_human):
        logger.debug('Forwarding client')
    else:
        play_audio(r'/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/src/Hangup_phrase.wav')
        logger.debug('Terminating Call')
