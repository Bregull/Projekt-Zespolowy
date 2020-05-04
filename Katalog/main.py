from input_data import *
from plot_spectrograms import *

fs, samples, file_name = data_input()
spectrogram(fs, samples, file_name)
mel_spectrogram(fs, samples, file_name)
