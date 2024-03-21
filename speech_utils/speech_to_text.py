import timeit

import torch

import torch
from peft import PeftModel, PeftConfig
from transformers import AutomaticSpeechRecognitionPipeline
from transformers import WhisperFeatureExtractor
from transformers import WhisperForConditionalGeneration
from transformers import WhisperTokenizer

from utils.logger import get_logging_config
import logging.config

logging.config.dictConfig(get_logging_config())
logger = logging.getLogger(__name__)


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
    logger.debug('Model loading complete')

    model.config.use_cache = True
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device("cpu")

    model.to(device)
    logger.debug('Building pipe')
    pipe = AutomaticSpeechRecognitionPipeline(model=model, tokenizer=tokenizer, feature_extractor=feature_extractor)
    return pipe


whisper_pipe = init_whisper_pipe()


def speech_to_text(path_to_mp3: str):
    with torch.cuda.amp.autocast():
        logger.debug('Starting speech recognition')
        result = whisper_pipe(path_to_mp3,
                              generate_kwargs={"language": "german"})
        return result['text']
