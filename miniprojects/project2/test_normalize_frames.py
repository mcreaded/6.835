import sys

from load_gestures import load_gestures
from normalize_frames import normalize_frames


if len(sys.argv) != 2:
    raise ValueError('Error! Give normalized frame number after filename in command. \n'
                     'e.g. python normalize_frames.py 20')

num_frames = int(sys.argv[1])

gesture_sets = load_gestures()
norm_gesture_sets = normalize_frames(gesture_sets, num_frames)

for ngs in norm_gesture_sets:
    for seq in ngs.sequences:
        if len(seq.frames) != num_frames:
            print(len(seq.frames))
            raise AssertionError("Not all frames are normalized")

print("Correct! All frames have been normalized.")