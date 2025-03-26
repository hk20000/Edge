import pyaudio
import wave

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
BUFFER = 1024 * 16
RECORD_SECONDS = 10
OUTPUT_FILE = "output.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open audio stream
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=BUFFER
)

print("Recording...")

# Record audio
frames = []
for _ in range(0, int(RATE / BUFFER * RECORD_SECONDS)):
    data = stream.read(BUFFER)
    frames.append(data)

print("Recording finished.")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save recorded audio
with wave.open(OUTPUT_FILE, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Audio saved to {OUTPUT_FILE}")