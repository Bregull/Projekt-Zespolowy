from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.models import Sequential
import pandas as pd
import numpy as np
import keras
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
import os


data_frame = pd.read_pickle("dataframe.pkl")

data = np.array(data_frame.data.tolist())
class_ID = np.array(data_frame.class_ID.tolist())

print(class_ID)

label_encoder = LabelEncoder()
class_category2 = to_categorical(class_ID)

data_train, data_test, class_train, class_test = train_test_split(data, class_ID, test_size=0.1, random_state=40)

print("Train shape: ", data_train.shape, ' ', class_train.shape)
print("Test shape: ", data_test.shape, '  ', class_test.shape)