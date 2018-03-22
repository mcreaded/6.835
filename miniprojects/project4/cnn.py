import keras
from keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D, AveragePooling2D
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
import numpy as np

num_classes = 7 #angry, disgust, fear, happy, sad, surprise, neutral
batch_size = 256
epochs = 5

# READ IN KAGGLE DATA
with open("data/kaggle_fer2013/fer2013.csv") as file:
     data = file.readlines()

lines = np.array(data)

x_train, y_train, x_test, y_test = [], [], [], []

# 1. A) SPLIT DATA INTO TEST AND TRAIN
for i in range(1,lines.size):
    emotion, img, usage = lines[i].split(",")
    val = img.split(" ")
    pixels = np.array(val, 'float32')
    emotion = keras.utils.to_categorical(emotion, num_classes)

    if 'Training' in usage:
        y_train.append(emotion)
        x_train.append(pixels)
    elif 'PublicTest' in usage:
        y_test.append(emotion)
        x_test.append(pixels)

print(len(x_train))
print(x_train[0])
print(len(y_train))

# 1. B) CAST AND NORMALIZE DATA

# 1. C) RESHAPE DATA

# 2. CREATE CNN MODEL
# input = Input(shape=(48, 48, 1, ))

# 3. A) DATA BATCH PROCESS

# 3. B) TRAIN AND SAVE MODEL

# model.save('my_model.h5')

