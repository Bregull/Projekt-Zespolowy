import record_import_wav
from scipy import signal
import matplotlib.pyplot as plt
import pylab

'''
jesteśmy w stanie wybrać czy chcemy nagrać, czy wybrać plik wav z dysky
r - nagraj -> przerwanie nagrania 'ctr + c'
i - wybierz z dysku

informacje są przedstawione w formie 
data - numpy array zawierający próbki
fs - częstotliwość próbkowania
'''

''' wykreśla nam spektrogram w formacie png'''


def plot_spectrogram(spectrogram_fs, spectrogram_samples):
    plt.figure(num=None, figsize=(19, 12))
    plt.title("Spectogram")
    plt.specgram(spectrogram_samples, Fs=spectrogram_fs)
    plt.savefig('spectrogram.png')


''' w zależności od wyboru nagrywa, lub wybiera .wav z dysku'''


def data_input():
    answer = input('record or import? (r/i): ')

    while answer != 'r' and answer != 'i':
        answer = input('Wrong input\nrecord or import? (r/i): ')

    if answer == 'r':
        input_fs, input_samples = record_import_wav.record()
    elif answer == 'i':
        input_fs, input_samples = record_import_wav.import_wav()
    else:
        return -1

    return input_fs, input_samples
