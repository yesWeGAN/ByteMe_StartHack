from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, AutomaticSpeechRecognitionPipeline
import torchaudio
import torch
import timeit

# Define the model and processor name
model_name = 'ss0ffii/whisper-small-german-swiss'

processor = Wav2Vec2Processor.from_pretrained(model_name, use_auth_token="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")
model = Wav2Vec2ForCTC.from_pretrained(model_name, use_auth_token="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")

if torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')
model.to(device)

pipe = AutomaticSpeechRecognitionPipeline(model=model, processor=processor, device=device.index)

# Load audio
speech, _ = torchaudio.load(r"/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/cornelia_arbeitsweg-1.mp3")

# Inference
start = timeit.default_timer()
result = pipe(speech, sampling_rate=16_000)
print(result["text"])
stop = timeit.default_timer()

print('Time: ', stop - start)