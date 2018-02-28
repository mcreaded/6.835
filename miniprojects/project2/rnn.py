import numpy as np
from keras.models import Model
from keras.layers import Input, LSTM, Dense, concatenate

from normalize_frames import normalize_frames
from load_gestures import load_gestures

# 9. FORMAT DATA
gesture_sets = load_gestures()
normalize_frames(gesture_sets, 36)

samples = []
labels = []

for gs in gesture_sets:
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
batch_size = 12
epochs = 100
latent_dim = 16

input_layer = Input(shape=(X.shape[1:]))
lstm = LSTM(latent_dim)(input_layer)
dense = Dense(latent_dim, activation='relu')(lstm)
pred = Dense(len(gesture_sets), activation='softmax')(dense)

model = Model(inputs=input_layer, outputs=pred)
model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=["acc"])

model.fit(X,
          Y,
          epochs=epochs,
          batch_size=batch_size,
          verbose=1,
          validation_split=0.3,
          shuffle=True)
