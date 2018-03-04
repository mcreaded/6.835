import numpy as np
from keras.models import Model
from keras.layers import Input, LSTM, Dense, concatenate

from normalize_frames import normalize_frames
from load_gestures import load_gestures

# 9. FORMAT DATA
gesture_sets = load_gestures()
_gesture_sets=normalize_frames(gesture_sets, 36)

samples = []
labels = []

for gs in _gesture_sets:
    for seq in gs.sequences:
        sample = np.vstack(list(map(lambda x: x.frame, seq.frames)))
        samples.append(sample)
        labels.append(gs.label)

X = np.array(samples)
Y = np.vstack(labels)

# Shuffle data
p = np.random.permutation(len(X))
X = X[p]
Y = Y[p]

# 10. CREATE AND TRAIN MODEL
def run_lstm(batch_size = 12,epochs = 100,latent_dim = 16):
  input_layer = Input(shape=(X.shape[1:]))
  lstm = LSTM(latent_dim)(input_layer)
  dense = Dense(latent_dim, activation='relu')(lstm)
  pred = Dense(len(gesture_sets), activation='softmax')(dense)

  model = Model(inputs=input_layer, outputs=pred)
  model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=["acc"])

  fit = model.fit(X,
            Y,
            epochs=epochs,
            batch_size=batch_size,
            verbose=1,
            validation_split=0.3,
            shuffle=True)
  return fit 
def run_bid_lstm(batch_size = 12,epochs = 100,latent_dim = 16):
  input_layer = Input(shape=(X.shape[1:]))
  lstm = LSTM(latent_dim)(input_layer)
  _lstm = LSTM(latent_dim,go_backwords=True)(input_layer)
  _merged = concatenate([lstm,_lstm],axis=0)
  dense = Dense(latent_dim, activation='relu')(_merged)
  pred = Dense(len(gesture_sets), activation='softmax')(dense)

  model = Model(inputs=input_layer, outputs=pred)
  model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=["acc"])

  fit = model.fit(X,
            Y,
            epochs=epochs,
            batch_size=batch_size,
            verbose=1,
            validation_split=0.3,
            shuffle=True)
  return fit

