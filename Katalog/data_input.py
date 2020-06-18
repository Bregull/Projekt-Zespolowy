import record_import_wav
import sys
'''
jesteśmy w stanie wybrać czy chcemy nagrać, czy wybrać plik wav z dysky
r - nagraj -> przerwanie nagrania 'ctr + c'
i - wybierz z dysku

informacje są przedstawione w formie 
data - numpy array zawierający próbki
fs - częstotliwość próbkowania


w zależności od wyboru nagrywa, lub wybiera .wav z dysku
'''

print('record or import? (r/i): ')

def data_input():
    for answer in sys.argv[1]:
        while answer != 'r' and answer != 'i':
            answer = input('Wrong input\nrecord or import? (r/i): ')

        if answer == 'r':
            input_fs, input_samples, file_name, file_path = record_import_wav.record()
        elif answer == 'i':
            input_fs, input_samples, file_name, file_path = record_import_wav.import_wav()
        else:
            return -1
        
    return input_fs, input_samples, file_name, file_path  # to wraca do maina

print(data_input())