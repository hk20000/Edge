import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq

# Parameters
BUFFER = 1024 * 16
RATE = 44100

# Load the audio file
INPUT_FILE = "output.wav"

with wave.open(INPUT_FILE, 'rb') as wf:
    channels = wf.getnchannels()
    sample_width = wf.getsampwidth()
    framerate = wf.getframerate()
    n_frames = wf.getnframes()
    audio_data = wf.readframes(n_frames)

# Convert audio data to NumPy array
audio_int = np.frombuffer(audio_data, dtype=np.int16)

# Divide into chunks for analysis
chunks = [audio_int[i:i+BUFFER] for i in range(0, len(audio_int), BUFFER)]

# Prepare plots
fig, (ax1, ax2) = plt.subplots(2, figsize=(7, 7))

x = np.arange(0, BUFFER)
xf = fftfreq(BUFFER, 1/RATE)[:BUFFER//2]

line, = ax1.plot(x, np.random.rand(BUFFER), '-', lw=2)
line_fft, = ax2.plot(xf, np.random.rand(BUFFER//2), '-', lw=2)

ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('volume')
ax1.set_ylim(-5000, 5000)
ax1.set_xlim(0, BUFFER)

ax2.set_title('SPECTRUM')
ax2.set_xlabel('Frequency')
ax2.set_ylabel('Log Magnitude')
ax2.set_ylim(0, 1000)
ax2.set_xlim(0, RATE/2)

plt.show(block=False)

# Analyze and plot
for chunk in chunks:
    if len(chunk) < BUFFER:  # Skip incomplete chunks
        break
    
    yf = fft(chunk)
    
    line.set_ydata(chunk)
    line_fft.set_ydata(2.0 / BUFFER * np.abs(yf[:BUFFER // 2]))
    
    fig.canvas.draw()
    fig.canvas.flush_events()

print("Analysis complete.")
