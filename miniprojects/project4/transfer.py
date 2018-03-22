from keras.preprocessing import image
from keras.models import Model, load_model
from keras.preprocessing.image import ImageDataGenerator

import numpy as np
from visualization_gui import plot_emotion_prediction


num_classes = 7 #angry, disgust, fear, happy, sad, surprise, neutral
batch_size = 7
epochs = 3

# model = load_model('model_2.h5')

