import recordSound
import importSound


'''
dużo błędów, do poprawy:
- ogarnij lepsze nazwy
- importSound nie potrafi odczytać formatu recordSound -> ogarnij formaty
- okno tkinter się nie zamyka
- duuuuużo sprzątania w kodzie
'''

answer = input('record or import? (r/i): ')

while answer != 'r' and answer != 'i':
    answer = input('Wrong input\nrecord or import? (r/i): ')

if answer == 'r':
    recordSound.record()
elif answer == 'i':
    importSound.importSound()