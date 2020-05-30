import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import librosa



''' wykreśla nam spektrogram w formacie png'''


def spectrogram(spectrogram_fs, spectrogram_samples, file_name):
    plt.figure(figsize=(10, 6))
    S = librosa.amplitude_to_db(np.abs(librosa.stft(spectrogram_samples)), ref=np.max)
    librosa.display.specshow(S, sr=spectrogram_fs, y_axis='linear', x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram of %s' % file_name)
    plt.savefig('spectrogram.png')
    plt.close()




''' wykreśla spektrogram melowy'''


def mel_spectrogram(spectrogram_fs, spectrogram_samples, file_name):
    # trim silent edges
    whale_song, _ = librosa.effects.trim(spectrogram_samples)

    n_fft = 2048
    hop_length = 512
    n_mels = 128

    S = librosa.feature.melspectrogram(whale_song, sr=spectrogram_fs, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
    S_DB = librosa.power_to_db(S, ref=np.max)

    plt.figure(figsize=(10, 6))
    librosa.display.specshow(S_DB, sr=spectrogram_fs, hop_length=hop_length, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title("Mel Spectrogram of %s" % file_name)
    plt.savefig('mel_spectrogram.png')

mel_spectrogram(44100, )
spectrogram(44100, )

