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
        voice="shimmer",
        input=answer
    )

    response.stream_to_file(speech_file_path)
    return speech_file_path


def compare_result_to_query(result_comparison: str) -> str:
    """
    Pass the results of our search to openai to evaluate if the result matches with the query
    :param result_comparison: A string with the response to, wether the search result matches the query
    :return: The text of the answer
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system",
             "content": " Du bist ein assistent und im Folgenden gibt es ein Query eines Users, und dazu einige"
             "Textausschnitte, die dazu passen könnten. Falls die Textausschnitte die Frage des Users beantworten können,"
             "antwortest du 'Match'. Falls die Textausschnitte nicht übereinstimmen, gebe 'kein Match' zurück."},
            {"role": "user", "content": result_comparison},
        ]
    )

    return response.choices[0].message.content


def summarize_search(search_results_summary: str) -> str:
    """
    Pass the results of our search to openai to summarize it
    :param search_results_summary: A string with all search results
    :return: The text of the answer
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system",
             "content": 'Im Folgenden gibt es ein Query eines Users, und dazu einige Textausschnitte, die dazu passen könnten. Falls die Textausschnitte'
                        ' die Frage des Users beantworten können, fasse in maximal zwei Sätzen nur die Inhalte aus den Textausschnitten zusammen, die zu'
                        ' dem Query des Users passen. Falls die Textausschnitte nicht übereinstimmen, gebe "kein Match" zurück.'},
            {"role": "user", "content": search_results_summary},
        ]
    )

    return response.choices[0].message.content


def check_satisfaction(customer_satisfaction_answer: str) -> str:
    """
    Pass the results of our search to openai to evaluate if the customer wants to be connected to a human
    :param customer_satisfaction_answer: A string with the response to, whether the customer was satisfied or not
    :return: The text of the answer
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system",
             "content": " Du bist ein assistent der herausfinden muss ob ein Nutzer zu einem menschlicher Mitarbeiter weitergeleitet werden möchtee oder nicht. Wenn du glaubst, dass"
                        "er weitergeleitet werden möchte antwortest du mit 'JA' sonst mit 'Nein'"},
            {"role": "user", "content": customer_satisfaction_answer},
        ]
    )

    return response.choices[0].message.content


def forward_to_employee(customer_redirection_prompt: dict) -> str:
    """
    Pass the results of our search to openai to summarize it
    :param search_results_summary: A dictionary consisting of Name, Amt und Telefonnummer
    :return: The text of the answer
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system",
             "content": " Du bist ein höflicher Assistent, der Clienten am Telefon zu einem passenden Ansprechpartner"
                        " weiterleiten soll. Du bekommst folgende drei Angaben: Name, Amt und Telefonnummer."
                        " Falls der Name nicht vorhanden sein sollte, nenne nur das Amt und die dazugehörige Telefonnummer."},
            {"role": "user", "content": str(customer_redirection_prompt)},
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    res = convert_question_to_text(r'/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/audio/2.mp3')
    # res = summarize_search('Wo ist die kirsch')
    print(res)
