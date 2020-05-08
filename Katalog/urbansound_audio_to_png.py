from tkinter import filedialog
import os
from matplotlib import pyplot as plt
import librosa.display
import librosa
import numpy as np

'''
Skrypt ten generuje nam spektrogramy z bazy danych urban sound.
skrypt uruchamiamy komendą python urbansound_get_files.py
Napisany jest w ten sposób, że zapisuje z wybranej przez nas lokalizacji
(Lokalizacją jest folder UrbanSound8K!) spektrogramy każdego z plików wav
ALE
zapisuje je do folderu w którym się aktualnie znajdujemy tworzac nowy folder UrbanSound_Spectrograms
i tu jest haczyk!
trzeba najpierw stworzyć konkretną ścieżkę w folderze Katalog:

UrbanSound_Spectrograms
    |-audio
        |-fold1
        |-fold2
        |-fold3
        |-fold4
        |-fold5
        |-fold6
        |-fold7
        |-fold8
        |-fold9
        |-fold10

Skrypt zapisuje tylko jeden rodzaj spektrogramu, więc po zrobieniu melowych, 
należy zamienić linijke nr 67 aby wygenerować spektrogramy liniowe.
'''


def get_file_paths():
    directory = filedialog.askdirectory(title="UrbanSound directory")
    audio_directory = directory + "/audio/"

    folder_names = []
    path_list = []

    for i in range(10):
        folder_names.append('fold%s/' % str(i + 1))

    for folder in folder_names:
        folder_content = []
        files = os.listdir(audio_directory + folder)
        for file in files:
            folder_content.append(audio_directory + folder + file)
        path_list.append(folder_content)
    return path_list


def loop_files(path_list):
    for folder in path_list:
        for file in folder:
            file_name = os.path.split(file)[1]
            file_name_no_extension = os.path.splitext(file_name)[0]
            temp_dir = str(file).split('/')
            temp_dir = temp_dir[-3:-1]
            sub_folders = '/'.join(temp_dir)
            out_path = 'UrbanSound_Spectrograms/' + sub_folders + '/' + file_name_no_extension
            if '.DS_Store' in file_name_no_extension:
                pass
            else:
                mel_spectrogram(file, out_path) ## TUTAJ TRZEBA ZAMIENIC na spectrogram(file, out_path)


def mel_spectrogram(file_path, output_path):
    file_name = os.path.split(file_path)[1]
    spectrogram_samples, spectrogram_fs = librosa.load(file_path)
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
    output_path += '.png'
    print(output_path)
    plt.savefig(output_path)
    plt.close()


def spectrogram(file_path, output_path):
    file_name = os.path.split(file_path)[1]
    spectrogram_samples, spectrogram_fs = librosa.load(file_path)


    plt.figure(figsize=(10, 6))
    S = librosa.amplitude_to_db(np.abs(librosa.stft(spectrogram_samples)), ref=np.max)
    librosa.display.specshow(S, sr=spectrogram_fs, y_axis='linear', x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram of %s' % file_name)
    output_path += '.png'
    print(output_path)
    plt.savefig(output_path)
    plt.close()


paths = get_file_paths()
loop_files(paths)