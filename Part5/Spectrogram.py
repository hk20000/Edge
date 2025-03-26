import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfilt
import librosa
import librosa.display

# Function to design a band-pass filter
def design_filter(lowfreq, highfreq, fs, order=3):
    nyq = 0.5 * fs
    low = lowfreq / nyq
    high = highfreq / nyq
    sos = butter(order, [low, high], btype='band', output='sos')
    return sos

# Parameters
LOW_FREQ = 19400
HIGH_FREQ = 19600
SAMPLING_RATE = 44100
BUFFER = 1024 * 16
INPUT_FILE = "output.wav"

# Load recorded audio
with wave.open(INPUT_FILE, 'rb') as wf:
    channels = wf.getnchannels()
    sample_width = wf.getsampwidth()
    framerate = wf.getframerate()
    n_frames = wf.getnframes()
    audio_data = wf.readframes(n_frames)

# Ensure the file is mono-channel
if channels > 1:
    raise ValueError("The script supports mono-channel audio files only.")

# Convert audio data to numpy array
audio_int = np.frombuffer(audio_data, dtype=np.int16)

# Apply band-pass filtering
sos = design_filter(LOW_FREQ, HIGH_FREQ, SAMPLING_RATE, order=3)
filtered_audio = sosfilt(sos, audio_int)

# Visualize original and filtered waveform
fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 6))
x = np.linspace(0, len(audio_int) / SAMPLING_RATE, len(audio_int))

# Plot original waveform
ax1.plot(x, audio_int, label="Original Audio")
ax1.set_title("Original Audio Waveform")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Amplitude")

# Plot filtered waveform
ax2.plot(x, filtered_audio, label="Filtered Audio", color='orange')
ax2.set_title("Filtered Audio Waveform (Band-Pass)")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Amplitude")
plt.tight_layout()
plt.show()

# Analyze using Librosa
y, sr = librosa.load(INPUT_FILE, sr=None)

# Spectrogram
S_full, phase = librosa.magphase(librosa.stft(y))
fig, (ax1, ax2) = plt.subplots(2, figsize=(7, 7))
ax1.plot(y)
ax1.set_xlabel('Samples')
ax1.set_ylabel('Amplitude')
img = librosa.display.specshow(librosa.amplitude_to_db(S_full, ref=np.max),
                                y_axis='log', x_axis='time', sr=sr, ax=ax2)
fig.colorbar(img, ax=ax2)
ax1.set(title='Time Series')
ax2.set(title='Spectrogram')
plt.show()

# Chroma Estimation
S = np.abs(librosa.stft(y, n_fft=4096)) ** 2
chroma = librosa.feature.chroma_stft(S=S, sr=sr)
fig, ax = plt.subplots(nrows=2, sharex=True)
img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                               y_axis='log', x_axis='time', ax=ax[0])
fig.colorbar(img, ax=[ax[0]])
ax[0].label_outer()
img = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax[1])
fig.colorbar(img, ax=[ax[1]])
ax[0].set(title='Power Spectrogram')
ax[1].set(title='Chromogram')
plt.show()

# Mel-Spectrogram
S_mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
fig, ax = plt.subplots()
S_mel_dB = librosa.power_to_db(S_mel, ref=np.max)
img = librosa.display.specshow(S_mel_dB, x_axis='time', y_axis='mel', sr=sr, fmax=8000, ax=ax)
fig.colorbar(img, ax=ax, format='%+2.0f dB')
ax.set(title='Mel-frequency spectrogram')
plt.show()

# MFCC
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
fig, ax = plt.subplots(nrows=2, sharex=True)
img = librosa.display.specshow(librosa.power_to_db(S, ref=np.max), x_axis='time', y_axis='mel', fmax=8000, ax=ax[0])
fig.colorbar(img, ax=[ax[0]])
ax[0].set(title='Mel Spectrogram')
ax[0].label_outer()
img = librosa.display.specshow(mfccs, x_axis='time', ax=ax[1])
fig
