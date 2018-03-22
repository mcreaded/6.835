from keras.preprocessing import image
from keras.models import Model, load_model

import numpy as np
from visualization_gui import plot_emotion_prediction


model = load_model('my_simple_model.h5')

img = image.load_img("test_data/jackman.png", grayscale=True, target_size=(48, 48))

x = image.img_to_array(img)
x = np.expand_dims(x, axis = 0)

x /= 255

custom = model.predict(x)
plot_emotion_prediction(custom[0])
