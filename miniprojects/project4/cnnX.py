import keras
from keras.layers import Input, Dense, Dropout, Flatten, Conv3D, MaxPool3D, Reshape
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model

import numpy as np

from data.iPhoneX.faces import face_samples

num_classes = 7 #angry, disgust, fear, happy, sad, surprise, neutral
batch_size = 12
epochs = 20

emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
# 9. READ IN iPHONE X DATA AND SHAPE
def compute_label(name):
  label = []
  for em in emotions:
    label.append(int(em==name));
  return label
side_value = 0.120

x_train = np.array([[zip(face_samples[sample][imotion]['x'],face_samples[sample][imotion]['y'],face_samples[sample][imotion]['z']) for imotion in face_samples[sample]] for sample in face_samples])+side_value
x_train = np.round(x_train.reshape(-1,1220,3)/(side_value*2)*24).astype(int)

y_train = np.array([[compute_label(imotion) for imotion in face_samples[sample]] for sample in face_samples]).reshape(-1,7)

######
##To voxels
######
_x_train = np.zeros((x_train.shape[0],24,24,24))

for sam in xrange(x_train.shape[0]):
  for cld in xrange(x_train[sam].shape[0]):
    x = x_train[sam][cld][0]
    y = x_train[sam][cld][1]
    z = x_train[sam][cld][2]

    _x_train[sam][x,y,z]+=1;
# 10. CREATE MODEL OF CHOICE

inp = Input(shape=(24, 24, 24));
shape = Reshape((24,24,24,1))(inp);
conv1 = Conv3D(64,5,activation='relu')(shape);
pool = MaxPool3D(pool_size=(2, 2, 2), strides=(1,1,1))(conv1);
flat = Flatten()(pool);
dense1 = Dense(128,activation='relu')(flat)
dense2 = Dense(7,activation='relu')(dense1)

# 11. TRAIN AND TEST MODEL
model = Model(inputs=inp,outputs=dense2);
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy']);
fit = model.fit(_x_train,y_train,epochs=10,
  batch_size=12,verbose=1,validation_split=.2,shuffle=True)
print fit.history
