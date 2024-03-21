import os
from pathlib import Path

from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def convert_question_to_text(path_to_mp3: str):
    """
    Call openai api to convert question to text
    :param path_to_mp3: Path to the input mp3
    :return: The converted text
    """
    assert os.path.isfile(path_to_mp3), "File does not exists"
    audio_file = open(path_to_mp3, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

    return transcription.text


def convert_answer_to_audio(answer: str, speech_output_dir) -> str:
    """
    Prepare the final answer by converting the answer to an audio file
    :param answer: The answer as text
    :return: The path to a mp3 file with the speech
    """
    speech_file_path = os.path.join(speech_output_dir, "speech.mp3")
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=answer
    )

    response.stream_to_file(speech_file_path)
    return speech_file_path


def summarize_search(search_results_summary: str) -> str:
    """
    Pass the results of our search to openai to summarize it
    :param search_results_summary: A string with all search results
    :return: The text of the answer
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "Du bist ein freundlicher, hilfsbereiter Mitarbeiter der Kanton Verwaltung von St Gallen in der Schweiz und"
                                          "möchtest Kunden bestmöglich ihre Suchergebnisse erklären. Du gibt kurze und präzise Antworten"},
            {"role": "user", "content": search_results_summary},
        ]
    )

    return response.choices[0].message.content


def check_satisfaction(customer_satisfaction_answer: str) -> str:
    """
    Pass the results of our search to openai to evaluate if the customer wants to be connected to a human
    :param search_results_summary: A string with the response to, whether the customer was satisfied or not
    :return: The text of the answer
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",
             "content": "Du bist ein assistent der nur mit 'JA' oder 'Nein' antwortet und evaluiert ob ein Kunde"
                        " mit einem menschlichen Mitarbeiter verbunden werden möchte.Du antwortest Ja wenn der Kunde unzufrieden ist, allerdings mit"
                        " Nein wenn er äußert, dass er auflegen möchte"},
            {"role": "user", "content": customer_satisfaction_answer},
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    res = convert_question_to_text(r'/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/audio/2.mp3')
    # res = summarize_search('Wo ist die kirsch')
    print(res)
