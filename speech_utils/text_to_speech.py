import os

import boto3

polly_client = boto3.Session(
    aws_access_key_id=os.environ.get("KEY_ID"),
    aws_secret_access_key=os.environ.get("KEY"),
    region_name='us-west-2').client('polly')
def synthesize_speech(text):
    response = polly_client.synthesize_speech(
        Engine='neural',  # added this line for NTTS
        VoiceId='Daniel',
        OutputFormat='mp3',
        Text=text)

    file = open('speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()


if __name__ == "__main__":
    synthesize_speech('Hallo, ich verwende AWS Polly, um diesen Text in Sprache zu konvertieren.')
