from keras.preprocessing import image
from keras.models import Model, load_model
from keras.preprocessing.image import ImageDataGenerator

import numpy as np
from visualization_gui import plot_emotion_prediction
import cnn


num_classes = 7 #angry, disgust, fear, happy, sad, surprise, neutral
batch_size = 7
epochs = 3

model = load_model('model_2.h5')
train_imgs = []
test_path = 'data/selfies/test/'
train_path = 'data/selfies/train/'
train_images = ['angry1.jpg','didgust1.jpg','fear1.jpg','happy1.jpg','neutral1.jpg','sad1.jpg','surprise1.jpg']
test_images = ['angry2.jpg','didgust2.jpg','fear2.jpg','happy2.jpg','neutral2.jpg','sad2.jpg','surprise2.jpg']
x_train =  [np.expand_dims(image.img_to_array(image.load_img(train_path+im,grayscale=True, target_size=(48, 48))),axis=0) for im in train_images]
x_test = [np.expand_dims(image.img_to_array(image.load_img(train_path+im,grayscale=True, target_size=(48, 48))),axis=0) for im in test_images]
order = ['angry','didgust','fear','happy','neutral','sad','surprise']
y_train = [cnn.compute_label(name) for name in order]
y_test = [cnn.compute_label(name) for name in order]

fit = model.fit(x_train,y_train,epochs=10, batch_size=6,verbose=1)
print fit.history
test_scores = model.evaluate(x_test,y_test)
print test_scores