import wave

from piper import PiperVoice

voice = PiperVoice.load("data/voices/en_US-bryce-medium.onnx")

with wave.open("data/piper_test.wav", "wb") as audio_file:
    voice.synthesize_wav(
        "Real Madrid is the greatest club in the world.",
        audio_file,
    )