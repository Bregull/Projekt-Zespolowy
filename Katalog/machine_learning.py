import numpy as np
import datetime
import tensorflow as tf
import database_extraction


urbansound_wav_directory, csv_metadata = database_extraction.get_metadata()
data_frame, X_train, y_train = database_extraction.process_csv_data(urbansound_wav_directory, csv_metadata)
print(X_train.shape)
print(y_train.shape)





model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(units=128, activation='relu', input_shape=(40, )))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(units=10, activation='softmax'))
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['sparse_categorical_accuracy'])
print(model.summary())
model.fit(X_train, y_train, epochs=5)

