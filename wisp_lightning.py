from lightning_whisper_mlx import LightningWhisperMLX

whisper = LightningWhisperMLX(model="distil-medium.en", batch_size=12, quant=None)

output = whisper.transcribe(audio_path="/test.mp4")

print(output)