import pyaudio
import wave

# Parameters
FORMAT = pyaudio.paInt16  # Audio format (16-bit int)
CHANNELS = 1              # Number of audio channels (1 for mono, 2 for stereo)
RATE = 44100              # Sampling rate in Hz
BUFFER = 1024             # Buffer size
RECORD_SECONDS = 10       # Duration to record
OUTPUT_FILE = "output.wav"  # Output file name

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

# Save the recorded audio to a file
with wave.open(OUTPUT_FILE, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Audio saved to {OUTPUT_FILE}")
