import pandas as pd
import librosa
import numpy as np
import os
from tkinter import filedialog
import skimage
from skimage import io

'''
converts metada .csv file from the UrbanSound8K library to .pkl format
'''
def scale_minmax(X, min=0.0, max=1.0):
    X_std = (X - X.min()) / (X.max() - X.min())
    X_scaled = X_std * (max - min) + min
    return X_scaled

def spectrogram_image(y, sr, out, hop_length, n_mels):
    # use log-melspectrogram
    mels = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels,
                                            n_fft=hop_length*2, hop_length=hop_length)
    mels = np.log(mels + 1e-9) # add small number to avoid log(0)

    # min-max scale to fit inside 8-bit range
    img = scale_minmax(mels, 0, 255).astype(np.uint8)
    img = np.flip(img, axis=0) # put low frequencies at the bottom in image
    img = 255-img # invert. make black==more energy
    print(img.shape)

    # save as PNG
    #skimage.io.imsave(out, img)

def extract_features(file_name): # returns mfcc data from file.
    try:
        # settings
        hop_length = 512  # number of samples per time-step in spectrogram
        n_mels = 128  # number of bins in spectrogram. Height of image
        time_steps = 384  # number of time-steps. Width of image

        # load audio. Using example from librosa
        y, sr = librosa.load(file_name, offset=0., duration=4.0, sr=22050)

        # extract a fixed length window
        start_sample = 0  # starting at beginning
        length_samples = time_steps * hop_length
        window = y[start_sample:start_sample + length_samples]
        print(window.shape)
        out = 'out.png'
        spectrogram_image(window, sr=sr, out=out, hop_length=hop_length, n_mels=n_mels)

    except Exception as e:
        print("Error encountered while parsing file: ", file_name)
        return None

    return window


def get_metadata():
    urban_sound_directory = filedialog.askdirectory(title="UrbanSound directory")
    metadata_directory = urban_sound_directory + '/metadata/UrbanSound8K.csv'
    urbansound_wav_directory = urban_sound_directory + '/audio/'


    csv_metadata = pd.read_csv(metadata_directory)

    return urbansound_wav_directory, csv_metadata



def process_csv_data(urbansound_wav_directory, csv_metadata):
    output_features = []
    waves_data = np.empty((0,40))
    list_data = np.empty((0,1))
    for item, row in csv_metadata.iterrows():
        file_name = os.path.join(os.path.abspath(urbansound_wav_directory) + '/' + 'fold' + str(row['fold']) + '/' + str(row['slice_file_name']))

        class_ID = row["classID"]
        wav_data = extract_features(file_name)
        #waves_data = np.append(waves_data, wav_data.reshape((1,40)), axis=0)
        #list_data = np.append(list_data, [class_ID])

        #output_features.append([wav_data, int(class_ID)])

    list_data = np.array(list_data)
    feature_dataframe = pd.DataFrame(data=output_features, columns=['data', 'class_ID'])
    feature_dataframe.to_pickle('dataframe.pkl')
    return feature_dataframe, waves_data, list_data

urbansound_wav_directory, csv_metadata = get_metadata()
data_frame = process_csv_data(urbansound_wav_directory, csv_metadata)