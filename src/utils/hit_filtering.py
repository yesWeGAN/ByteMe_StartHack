def filter_hits_threshold(questions: list[str],answers: list[str], scores: list[float], threshold: float) -> tuple[list[str], list[str]]:

    filtered = [(q, a) for q, a, s in zip(questions,answers, scores) if s > threshold]
    return zip(*filtered)

def create_summary_str(questions: list[str], answers: list[str],original_question:str):

    summary_str = ['\n\n']
    for question, answer in zip(questions, answers):
        summary_str.append(f'{question}: {answer}\n')
    summary_str = ''.join(summary_str)
    summary_str = original_question + summary_str

    return summary_str
