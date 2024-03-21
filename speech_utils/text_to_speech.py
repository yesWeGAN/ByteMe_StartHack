import os

import boto3

import simpleaudio as sa
import logging.config

from utils.logger import get_logging_config

logging.config.dictConfig(get_logging_config())
logger = logging.getLogger(__name__)

polly_client = boto3.Session(
    aws_access_key_id=os.environ.get("KEY_ID"),
    aws_secret_access_key=os.environ.get("KEY"),
    region_name='us-west-2').client('polly')
def synthesize_speech(text,output_dir):
    logger.debug('Synthesizing text')
    response = polly_client.synthesize_speech(
        Engine='neural',  # added this line for NTTS
        VoiceId='Daniel',
        OutputFormat='mp3',
        Text=text)

    output_path =os.path.join(output_dir,'speech.mp3')
    file = open(output_path, 'wb')
    file.write(response['AudioStream'].read())
    file.close()
    logger.debug(f'Wrote audio to {output_path}')
    return output_path

def play_audio(file_name):
    logger.debug('Trying to play audio')
    wave_obj = sa.WaveObject.from_wave_file(file_name)
    play_obj = wave_obj.play()
    play_obj.wait_done()



if __name__ == "__main__":
    synthesize_speech('Hallo, ich verwende AWS Polly, um diesen Text in Sprache zu konvertieren.')
