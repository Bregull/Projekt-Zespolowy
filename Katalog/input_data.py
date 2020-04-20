import record_import_wav
from scipy import signal
import matplotlib.pyplot as plt
import pylab

'''
jesteśmy w stanie wybrać czy chcemy nagrać, czy wybrać plik wav z dysky
r - nagraj
i - wybierz z dysku

informacje są przedstawione w formie 
data - numpy array zawierający próbki
fs - częstotliwość próbkowania
'''


def plot_spectrogram(fs, samples):
    pylab.figure(num=None, figsize=(19, 12))
    pylab.subplot(111)
    pylab.title('spectrogram of')
    pylab.specgram(samples, Fs=fs)
    pylab.savefig('spectrogram.png')


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


fs, samples = data_input()
plot_spectrogram(fs, samples)
