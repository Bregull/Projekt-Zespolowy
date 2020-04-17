import record_import_wav

'''
jesteśmy w stanie wybrać czy chcemy nagrać, czy wybrać plik wav z dysky
r - nagraj
i - wybierz z dysku

informacje są przedstawione w formie 
data - numpy array zawierający próbki
fs - częstotliwość próbkowania
'''
answer = input('record or import? (r/i): ')

while answer != 'r' and answer != 'i':
    answer = input('Wrong input\nrecord or import? (r/i): ')

if answer == 'r':
    fs, data = record_import_wav.record()
elif answer == 'i':
    fs, data = record_import_wav.import_wav()
