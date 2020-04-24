import pyaudio
import wave
from tkinter import filedialog
from scipy.io.wavfile import read
import numpy as np


def get_wav(file_path):
    wave_file = wave.open(file_path, 'r')
    channels = wave_file.getnchannels()

    (fs, data) = read(file_path)

    if channels == 2:
        out_data = np.sum([data[:, 0], data[:, 1]], axis=0)
    elif channels == 1:
        out_data = data
    else:
        raise TypeError("Only Mono or Stereo .wav files are accepted")



    return fs, out_data


def record():
    chunk = 512
    coding_format = pyaudio.paInt32
    channels = 1
    sampling_rate = 44100
    file_path = 'recording.wav'

    p = pyaudio.PyAudio()

    stream = p.open(format=coding_format,
                    channels=channels,
                    rate=sampling_rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("* recording")
    frames = []

    while 1:
        try:
            data = stream.read(chunk)
            frames.append(data)
        except KeyboardInterrupt:
            data = stream.read(chunk)
            frames.append(data)
            break

    print("* done recording")

    stream.stop_stream()
    stream.close()

    p.terminate()

    wave_file = wave.open(file_path, 'wb')
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(p.get_sample_size(coding_format))
    wave_file.setframerate(sampling_rate)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

    fs, data = get_wav(file_path)
    return fs, data


def import_wav():
    file_path = filedialog.askopenfilename()

    if file_path.lower().endswith('.wav'):
        fs, data = get_wav(file_path)
    else:
        raise TypeError("Only Mono or Stereo .wav files are acceptable")
    return fs, data
