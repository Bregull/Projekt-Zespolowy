import pandas as pd
import librosa
import numpy as np
import os
from tkinter import filedialog

'''
converts metada .csv file from the UrbanSound8K library to .pkl format
'''

def extract_features(file_name): # returns mfcc data from file.
    try:
        audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        mfccsscaled = np.mean(mfccs.T, axis=0)


    except Exception as e:
        print("Error encountered while parsing file: ", file_name)
        return None

    return mfccsscaled


def get_metadata():
    urban_sound_directory = filedialog.askdirectory(title="UrbanSound directory")
    metadata_directory = urban_sound_directory + '/metadata/UrbanSound8K.csv'
    urbansound_wav_directory = urban_sound_directory + '/audio/'


    csv_metadata = pd.read_csv(metadata_directory)

    return urbansound_wav_directory, csv_metadata



def process_csv_data(urbansound_wav_directory, csv_metadata):
    output_features = []
    #waves_data = np.empty((0,40))
    #list_data = np.empty((0,1))
    for item, row in csv_metadata.iterrows():
        file_name = os.path.join(os.path.abspath(urbansound_wav_directory) + '/' + 'fold' + str(row['fold']) + '/' + str(row['slice_file_name']))

        class_ID = row["classID"]
        wav_data = extract_features(file_name)
        #waves_data = np.append(waves_data, wav_data.reshape((1,40)), axis=0)
        #list_data = np.append(list_data, [class_ID])

        output_features.append([wav_data, int(class_ID)])

    #list_data = np.array(list_data)
    feature_dataframe = pd.DataFrame(data=output_features, columns=['data', 'class_ID'])
    feature_dataframe.to_pickle('dataframe.pkl')
    return feature_dataframe

#urbansound_wav_directory, csv_metadata = get_metadata()
#data_frame = process_csv_data(urbansound_wav_directory, csv_metadata)

