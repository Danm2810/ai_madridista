import time

import torch
import torchaudio
from chatterbox.tts_turbo import ChatterboxTurboTTS

import sounddevice as sd

print("Loading Chatterbox-Turbo...")
model = ChatterboxTurboTTS.from_pretrained(device="cuda")
print("Model loaded.")

text = (
    "You keep telling me Barcelona play beautiful football. "
    "Lovely. Put that on a postcard. "
    "When the match gets ugly and the pressure starts rising, "
    "I know which shirt I want my team wearing. "
    "Real Madrid do not need your approval. We need another trophy."
)

sentences = [
    "You keep telling me Barcelona play beautiful football.",
    "Lovely. Put that on a postcard.",
    "When the match gets ugly and the pressure starts rising...",
    "I know which shirt I want my team wearing.",
    "Real Madrid do not need your approval. We need another trophy.",
]

for number, sentence in enumerate(sentences, start=1):
    torch.cuda.synchronize()
    start = time.perf_counter()

    audio = model.generate(
        sentence,
        audio_prompt_path=r"C:\Users\Daniel Mikhail\Downloads\demoman.wav",
    )

    torch.cuda.synchronize()
    samples = audio.squeeze(0).cpu().numpy()
    elapsed = time.perf_counter() - start
    print(f"Sentence {number} generated in {elapsed:.2f} seconds.")

    sd.wait()
    sd.play(samples, samplerate=model.sr)

sd.wait()