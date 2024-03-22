def filter_hits_threshold(questions: list[str], answers: list[str]) -> tuple[list[str], list[str]]:
    filtered = [(q, a) for q, a in zip(questions, answers)]
    return zip(*filtered)


def create_summary_str(questions: list[str], answers: list[str], original_question: str):
    summary_str = ['\n\n']
    for question, answer in zip(questions, answers):
        summary_str.append(f'{question}: {answer}\n')
    summary_str = ''.join(summary_str)
    summary_str = original_question + summary_str

    return summary_str


def find_contact(contact_url: str, contact_dict: dict):
    pass
