import timeit

import torch

import torch
from peft import PeftModel, PeftConfig
from transformers import AutomaticSpeechRecognitionPipeline
from transformers import WhisperFeatureExtractor
from transformers import WhisperForConditionalGeneration
from transformers import WhisperTokenizer


def init_whisper_pipe():
    model_name_or_path = "openai/whisper-large-v3"
    task = "transcribe"
    feature_extractor = WhisperFeatureExtractor.from_pretrained(model_name_or_path)
    tokenizer = WhisperTokenizer.from_pretrained(model_name_or_path, task=task)

    peft_model_id = "flurin17/whisper-large-v3-peft-swiss-german"  # Use the same model ID as before.
    peft_config = PeftConfig.from_pretrained(peft_model_id)
    model = WhisperForConditionalGeneration.from_pretrained(
        peft_config.base_model_name_or_path, load_in_8bit=True, device_map="auto"
    )
    model = PeftModel.from_pretrained(model, peft_model_id)

    model.config.use_cache = True
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device("cpu")

    model.to(device)

    pipe = AutomaticSpeechRecognitionPipeline(model=model, tokenizer=tokenizer, feature_extractor=feature_extractor)
    return pipe


whisper_pipe = init_whisper_pipe()


def speech_to_text():
    with torch.cuda.amp.autocast():
        result = whisper_pipe(r"/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/cornelia_arbeitsweg-1.mp3",
                              generate_kwargs={"language": "german"})
