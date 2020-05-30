import numpy as np
import pandas as pd
import os
import librosa
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, Conv2D, MaxPooling2D, GlobalAveragePooling2D
import matplotlib.pyplot as plt
import tensorflow as tf



max_pad_len = 174

def extract_features(file_name):
    try:
        audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast', duration=4)
        print(audio.shape)
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        pad_width = max_pad_len - mfccs.shape[1]
        print(pad_width)
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')

    except Exception as e:
        print("Error encountered while parsing file: ", file_name)
        return None

    return mfccs

def extract_metadata():
    if os.path.isfile('conv/X_array.npy') and os.path.isfile('conv/y_array.npy'):
        X = np.load('conv/x_array.npy')
        y = np.load('conv/y_array.npy')

        return X, y

    else:
        # Set the path to the full UrbanSound dataset

        fulldatasetpath = '/Users/jacekfica/Desktop/UrbanSound8K/audio/'

        metadata = pd.read_csv('/Users/jacekfica/Desktop/UrbanSound8K/metadata/UrbanSound8K.csv')

        features = []

        # Iterate through each sound file and extract the features
        for index, row in metadata.iterrows():
            file_name = os.path.join(
                os.path.abspath(fulldatasetpath) + '/' + 'fold' + str(row['fold']) + '/' + str(row['slice_file_name']))

            class_label = row["classID"]
            data = extract_features(file_name)

            features.append([data, int(class_label)])

        # Convert into a Panda dataframe
        featuresdf = pd.DataFrame(features, columns=['feature', 'class_label'])

        print('Finished feature extraction from ', len(featuresdf), ' files')



        # Convert features and corresponding classification labels into numpy arrays
        X = np.array(featuresdf.feature.tolist())
        y = np.array(featuresdf.class_label.tolist())

        os.mkdir("conv")
        np.save('conv/X_array.npy', X)
        np.save('conv/y_array.npy', y)

        return X, y



num_rows = 40
num_columns = 174
num_channels = 1



X, y = extract_metadata()

# Encode the classification labels
le = LabelEncoder()
yy = to_categorical(le.fit_transform(y))



x_train, x_test, y_train, y_test = train_test_split(X, yy, test_size=0.2, random_state = 42)

x_train = x_train.reshape(x_train.shape[0], num_rows, num_columns, num_channels)
x_test = x_test.reshape(x_test.shape[0], num_rows, num_columns, num_channels)

num_labels = yy.shape[1]
filter_size = 2

'''
# Construct model
model = Sequential()
model.add(Conv2D(filters=16, kernel_size=2, input_shape=(num_rows, num_columns, num_channels), activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))

model.add(Conv2D(filters=32, kernel_size=2, activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))

model.add(Conv2D(filters=64, kernel_size=2, activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))

model.add(Conv2D(filters=128, kernel_size=2, activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))
model.add(GlobalAveragePooling2D())

model.add(Dense(num_labels, activation='softmax'))

model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

# Display model architecture summary
model.summary()

# Calculate pre-training accuracy
score = model.evaluate(x_test, y_test, verbose=1)
accuracy = 100*score[1]

print("Pre-training accuracy: %.4f%%" % accuracy)

from keras.callbacks import ModelCheckpoint
from datetime import datetime

#num_epochs = 12
#num_batch_size = 128

num_epochs = 72
num_batch_size = 256

checkpointer = ModelCheckpoint(filepath='weights.best.basic_cnn.hdf5',
                               verbose=1, save_best_only=True)
start = datetime.now()

history = model.fit(x_train, y_train, batch_size=num_batch_size, epochs=num_epochs, validation_data=(x_test, y_test), callbacks=[checkpointer], verbose=1)


duration = datetime.now() - start
print("Training completed in time: ", duration)

# Evaluating the model on the training and testing set/
score = model.evaluate(x_train, y_train, verbose=0)
print("Training Accuracy: ", score[1])

score = model.evaluate(x_test, y_test, verbose=0)
print("Testing Accuracy: ", score[1])



print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

'''

model = tf.keras.models.load_model('weights.best.basic_cnn.hdf5')

# Show the model architecture
model.summary()

loss, acc = model.evaluate(x_test,  y_test, verbose=2)
print('Restored model, accuracy: {:5.2f}%'.format(100*acc))




def print_prediction(file_name):
    prediction_feature = extract_features(file_name)
    prediction_feature = prediction_feature.reshape(1, num_rows, num_columns, num_channels)

    predicted_vector = model.predict_classes(prediction_feature)
    predicted_class = le.inverse_transform(predicted_vector)
    print("The predicted class is:", predicted_class[0], '\n')

    predicted_proba_vector = model.predict_proba(prediction_feature)
    predicted_proba = predicted_proba_vector[0]
    for i in range(len(predicted_proba)):
        category = le.inverse_transform(np.array([i]))
        print(category[0], "\t\t : ", format(predicted_proba[i], '.32f') )




print('dzieci')
print_prediction('/Users/jacekfica/Desktop/testy/dzieci.wav')
print('auto')
print_prediction('/Users/jacekfica/Desktop/testy/auto.wav')
print('klima')
print_prediction('/Users/jacekfica/Desktop/testy/klima.wav')
print('mlotek')
print_prediction('/Users/jacekfica/Desktop/testy/mlotek.wav')
print('psy')
print_prediction('/Users/jacekfica/Desktop/testy/psy.wav')
print('psy')
print_prediction('/Users/jacekfica/Desktop/testy/psy1.wav')
print('psy')
print_prediction('/Users/jacekfica/Desktop/testy/psy2.wav')
print('shot')
print_prediction('/Users/jacekfica/Desktop/testy/shot.wav')
print('silnik')
print_prediction('/Users/jacekfica/Desktop/testy/silnik.wav')
print('muzyka ulicy')
print_prediction('/Users/jacekfica/Desktop/testy/street_music.wav')
print('syrena')
print_prediction('/Users/jacekfica/Desktop/testy/syrena.wav')
print('wiercenie')
print_prediction('/Users/jacekfica/Desktop/testy/wiercenie.wav')

