import pyaudio
import wave

def record():

    chunk = 512
    coding_format = pyaudio.paInt32
    channels = 1
    sampling_rate = 44100
    output_wave_filename = 'test.wav'

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

    wave_file = wave.open(output_wave_filename, 'wb')
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(p.get_sample_size(coding_format))
    wave_file.setframerate(sampling_rate)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()
