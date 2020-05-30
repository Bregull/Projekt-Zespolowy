import numpy as np
import datetime
import tensorflow as tf
import database_extraction
import errno
import os
import matplotlib.pyplot as plt



def metadane():
    if os.path.isfile('input.csv') and os.path.isfile('output.csv'):
        X_train = np.loadtxt('input.csv', delimiter=',')
        y_train = np.loadtxt('output.csv', delimiter=',')
        return X_train, y_train
    else:
        urbansound_wav_directory, csv_metadata = database_extraction.get_metadata()
        data_frame, X_train, y_train = database_extraction.process_csv_data(urbansound_wav_directory, csv_metadata)
        np.savetxt('input.csv', X_train, delimiter=',')
        np.savetxt('output.csv', y_train, delimiter=',')
        return X_train, y_train


x_train, y_train = metadane()


model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(units=256, activation='relu', input_shape=(40, )))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(units=128, activation='relu'))
model.add(tf.keras.layers.Dense(units=64, activation='relu'))
model.add(tf.keras.layers.Dense(units=10, activation='softmax'))
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
print(model.summary())
history = model.fit(x_train, y_train, batch_size=10, epochs=100, verbose=1, validation_split=0.15)

print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('accuracy_ann.png')
plt.show()


# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('loss_ann.png')
plt.show()






