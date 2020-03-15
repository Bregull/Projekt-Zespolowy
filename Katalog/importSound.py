import pyaudio
import wave
from tkinter import filedialog

def importSound():
    chunk = 512

    p = pyaudio.PyAudio()

    file_path = filedialog.askopenfilename()
    wave_file = wave.open(file_path, 'rb')


    data = wave_file.readframes(chunk)

    stream = p.open(format=p.get_format_from_width(wave_file.getsampwidth()),
                    channels=wave_file.getnchannels(),
                    rate=wave_file.getframerate(),
                    output=True)


    while data != '':
        stream.write(data)
        data = wave_file.readframes(chunk)

    stream.stop_stream()
    stream.close()

    p.terminate()