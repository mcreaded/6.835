
def frames_to_remove(frames,num_remove):
	step =  frames/num_remove;
	offset = (step+frames%num_remove)/2;
	return [offset+i*step for i in range(num_remove)]
def frames_to_duplicate(frames,total=30):
	missing = total-frames
	step = frames/missing;
	offset = (frames%missing)/2
	return [offset+i*step for i in range(missing)]
def normalize_seq(sequence,num_frames):
	frames = len(sequence.frames)
	_frames = []
	if frames==num_frames:
		return
	if frames>=num_frames:
		to_remove = frames-num_frames
		rm = frames_to_remove(frames,to_remove)
		#print "remove: ",rm
		indices = sorted(list(set(range(frames))-set(rm)))
		_frames = [sequence.frames[i] for i in indices]
	else:
		added = frames_to_duplicate(frames,total=num_frames)
		indices = sorted(range(frames)+added)
		_frames = [sequence.frames[i] for i in indices]
	#print "resulting",len(_frames), "original: ",frames
	sequence.frames = _frames[0:]



def normalize_frames(gesture_sets, num_frames):
    """
    Normalizes the number of Frames in each Sequence in each GestureSet
    :param gesture_sets: the list of GesturesSets
    :param num_frames: the number of frames to normalize to
    :return: a list of GestureSets where all Sequences have the same number of Frames
    """
    from copy import deepcopy as dc 

    _gesture_sets = dc(gesture_sets)
   
    [[normalize_seq(seq,num_frames) for seq in gs.sequences] for gs in _gesture_sets]

    return _gesture_sets

    
