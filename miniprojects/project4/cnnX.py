import keras
from keras.layers import Input, Dense, Dropout, Flatten, Conv3D, MaxPool3D
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model

import numpy as np

from data.iPhoneX.faces import face_samples

num_classes = 7 #angry, disgust, fear, happy, sad, surprise, neutral
batch_size = 12
epochs = 20

emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

# 9. READ IN iPHONE X DATA AND SHAPE

# 10. CREATE MODEL OF CHOICE

# 11. TRAIN AND TEST MODEL
