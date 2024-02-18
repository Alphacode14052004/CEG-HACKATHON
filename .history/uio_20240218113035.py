import sounddevice as sd
import numpy as np
import vosk 
import wavio as wv

# Sampling frequency
freq = 16000  # Vosk model typically uses 16 kHz sample rate

# Recording duration
duration = 5

# Start recorder with the given values of duration and sample frequency
recording = sd.rec(int(duration * freq), samplerate=freq, channels=1, dtype=np.int16)

# Record audio for the given number of seconds
sd.wait()

# Create a Vosk model
model = vosk.Model(r"C:\Users\jimve\Documents\CEG-HACKATHON\vosk-model-small-en-us-0.15")

# Perform speech recognition directly on the recorded audio
result = model.recognize(recording, freq)

# Print the recognized text
print(result["text"])