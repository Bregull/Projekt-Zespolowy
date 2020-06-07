import pandas as pd
import librosa
import numpy as np
import os
from tkinter import filedialog
from pathlib import Path
from PIL import Image
from shutil import copyfile, rmtree

'''
Uruchamiamy wywołując kolejno każdą z funkcji. np.

png, csv = get_metadata()
process_csv_data(png, csv)
divide_pngs()
delete_unnecessary_folders()

otwiera się okno, wybieramy folder w którym znajdują się nasze spektrogramy
'''
def get_metadata():
    urban_sound_directory = filedialog.askdirectory(title="UrbanSound directory")
    metadata_directory = urban_sound_directory + '/metadata/UrbanSound8K.csv'
    urbansound_png_directory = urban_sound_directory + '/audio/'


    csv_metadata = pd.read_csv(metadata_directory)

    return urbansound_png_directory, csv_metadata



def process_csv_data(urbansound_png_directory, csv_metadata):
    if not os.path.isdir('pngs'):
        try:
            os.mkdir('pngs/')
        except Exception as e:
            print(f"Exception found {e}")
    for item, row in csv_metadata.iterrows():
        file_name = os.path.join(os.path.abspath(urbansound_png_directory) + '/' + 'fold' + str(row['fold']) + '/' + str(row['slice_file_name']))
        file_name_no_extension = file_name.split('.')
        png_path = file_name_no_extension[0] + '.png'
        png_name = os.path.basename(png_path)
        print(png_name)
        class_name = row["class"]

        image = Image.open(png_path)
        image_cropped = image.crop((125, 72, 745, 534))
        #image_cropped.show()

        if not os.path.isdir('pngs/' + class_name):
            try:
                os.mkdir('pngs/' + class_name)
            except Exception as e:
                print(f"Exception found {e}")
        try:
            image_cropped.save(f'pngs/{class_name}/{png_name}')
        except Exception as e:
            print(f"Exception found {e}")


def divide_pngs():
    try:
        os.mkdir(f'pngs/train')
        os.mkdir(f'pngs/test')
    except Exception as e:
        print(f'Exception found: {e}')
    folder_list = os.listdir('pngs')
    for folder in folder_list:
        threshold = int(len(os.listdir(f'pngs/{folder}')) * 4 / 5)
        all_files_in_current_folder = os.listdir(f'pngs/{folder}')
        if folder == 'test' or folder == 'train':
            break
        for i in range(len(all_files_in_current_folder)):
            print(all_files_in_current_folder[i])

            if i < threshold:
                try:
                    os.mkdir(f'pngs/train/{folder}')
                except Exception as e:
                    print(f'Exception found: {e}')
                copyfile(f'pngs/{folder}/{all_files_in_current_folder[i]}',
                         f'pngs/train/{folder}/{all_files_in_current_folder[i]}')
            else:
                try:
                    os.mkdir(f'pngs/test/{folder}')
                except Exception as e:
                    print(f'Exception found: {e}')
                copyfile(f'pngs/{folder}/{all_files_in_current_folder[i]}',
                         f'pngs/test/{folder}/{all_files_in_current_folder[i]}')

def delete_unnecessary_folders():
    for folder in os.listdir('pngs'):
        if folder != 'test' and folder != 'train':
            rmtree(f'pngs/{folder}')


