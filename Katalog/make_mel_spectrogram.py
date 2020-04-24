import librosa.display

import numpy as np
import matplotlib.pyplot as plt

filename = 'police_car.wav'

y, sr = librosa.load(filename)
# trim silent edges
whale_song, _ = librosa.effects.trim(y)

n_fft = 2048
hop_length = 512
n_mels = 128

S = librosa.feature.melspectrogram(whale_song, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
S_DB = librosa.power_to_db(S, ref=np.max)

plt.figure(figsize=(10, 6))
librosa.display.specshow(S_DB, sr=sr, hop_length=hop_length, x_axis='time', y_axis='mel')
plt.colorbar(format='%+2.0f dB')
plt.show()