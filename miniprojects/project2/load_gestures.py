import scipy.io
from Gesture import GestureSet, Sequence, Frame

def load_gestures():
    Gestures = scipy.io.loadmat('gesture_dataset.mat')
    gestures = Gestures['gestures']

    gesture_sets = []

    for index, raw_sequences in enumerate(gestures[0]):
        sequences = []
        for sequence in raw_sequences[0]:
            frames = []
            for i in range(sequence.shape[1]):
                temp = [f[i] for f in sequence]
                frames.append(Frame(temp))
            sequences.append(Sequence(frames, index))
        gesture_sets.append(GestureSet(sequences, index))

    return gesture_sets