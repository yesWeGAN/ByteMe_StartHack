import timeit

model_name_or_path = "openai/whisper-large-v3"
task = "transcribe"
from transformers import WhisperFeatureExtractor
from transformers import WhisperTokenizer
import torch
from peft import PeftModel, PeftConfig
from transformers import WhisperForConditionalGeneration

feature_extractor = WhisperFeatureExtractor.from_pretrained(model_name_or_path)
tokenizer = WhisperTokenizer.from_pretrained(model_name_or_path, task=task)



peft_model_id = "flurin17/whisper-large-v3-peft-swiss-german"  # Use the same model ID as before.
peft_config = PeftConfig.from_pretrained(peft_model_id)
model = WhisperForConditionalGeneration.from_pretrained(
    peft_config.base_model_name_or_path, load_in_8bit=True, device_map="auto"
)
model = PeftModel.from_pretrained(model, peft_model_id)

model.config.use_cache = True
if torch.cuda.is_available():
    device = torch.device('cuda')

model.to(device)

from transformers import AutomaticSpeechRecognitionPipeline

pipe = AutomaticSpeechRecognitionPipeline(model=model, tokenizer=tokenizer, feature_extractor=feature_extractor)

start = timeit.default_timer()
with torch.cuda.amp.autocast():
    result = pipe(r"/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/cornelia_arbeitsweg-1.mp3",
                  generate_kwargs={"language": "german"})
print(result["text"])
stop = timeit.default_timer()

print(stop - start)
