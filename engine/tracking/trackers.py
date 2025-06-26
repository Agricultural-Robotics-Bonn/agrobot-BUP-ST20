"""

"""

import numpy as np
import os
import pickle
from skimage.io import imread
import yaml

# bytetrack library must be installed!
from ByteTrack.yolox.tracker.matching import iou_distance

# from our library
from engine.tracking.matching import dynamicradius_distance, dynamicelipse_distance_delta, dynamicelipse_distance_sigma
import engine.tracking.ourtracker as ourtracker
from engine.tracking.bytetracker import Dynamic_BYTETracker

# the basic call function.
def base_creator(flags):
  # do bytetrack.
  if flags.usebytetrack:
    create_bytetrack_txts(flags)
  # do our tracker.
  else:
    create_ourtracker_txts(flags)

# get the criterion for the matching component
def get_criterion( criterion ):
  if criterion == 'default':
    return iou_distance
  elif criterion == 'dr':
    return dynamicradius_distance
  elif criterion == 'dre_delta':
    return dynamicelipse_distance_delta
  elif criterion == 'dre_sigma':
    return dynamicelipse_distance_sigma
  else:
    assert False, f'The criterion {criterion} does not currently exist.'

# tracking using bytetrack and creating the output txt files
def create_bytetrack_txts(flags):
  # get the sequence information.
  with open(flags.yaml) as fid:
    seqns = yaml.load(fid, Loader=yaml.FullLoader)
  with open(flags.image_yaml) as fid:
    fpseq = yaml.load(fid, Loader=yaml.FullLoader)
  # get the skip sequence information if required
  skips = None
  if flags.skip_files is not None:
    with open(flags.skip_files, 'rb') as fid:
      skips = pickle.load(fid)
  # create the output directory
  os.makedirs(flags.output_root, exist_ok=True)
  # now do the tracking.
  for s in seqns['eval']:
    print(f'Current sequence is:{s}')
    fout = open(os.path.join(flags.output_root, str(s)+'.txt'), 'w')
    # are we skipping?
    if skips is not None:
      files = skips[s]
    else:
      files = fpseq[s]
    # create the tracker
    tracker = Dynamic_BYTETracker(flags, get_criterion(flags.distance_criteria))
    # go over the files in the current sequence
    for f in files:
      # read in the image and get the shape
      path = os.path.join(flags.image_loc, str(s), f'{f}.tiff')
      img = imread(path, plugin='pil')
      imgshp = img.shape
      # get the mask2former outputs
      with open(os.path.join(flags.m2f, str(s), str(f)+'.pkl'), 'rb') as fid:
        data = pickle.load(fid)
      if len(data.keys())>0:
        inputs = []
        for k, v in data.items():
          bbox = v['bbox']
          inputs.append([bbox[0],bbox[1],bbox[0]+bbox[2],bbox[1]+bbox[3], 1.])
        tracks = tracker.update(np.array(inputs), [imgshp[0], imgshp[1]], [imgshp[0], imgshp[1]])
        for t in tracks:
          id = t.track_id
          bb = t.tlwh
          fout.write(f'{f},{id},{bb[0]},{bb[1]},{bb[2]},{bb[3]},{t.score}\n')
    fout.close()


# get the criteria for our trackers
def get_my_criterion(criteria):
  if criteria == 'default':
    return ourtracker.iou_distance
  elif criteria == 'dr':
    return ourtracker.dr_distance
  elif criteria == 'dre_delta':
    return ourtracker.dre_delta
  else:
    assert False, f'The criterion {criterion} does not currently exist.'

# tracking using our tracker and creating the output txt files.
def create_ourtracker_txts(flags):
  # get the sequence information.
  with open(flags.yaml) as fid:
    seqns = yaml.load(fid, Loader=yaml.FullLoader)
  with open(flags.image_yaml) as fid:
    fpseq = yaml.load(fid, Loader=yaml.FullLoader)
  # get the skip sequence information if required
  skips = None
  if flags.skip_files is not None:
    with open(flags.skip_files, 'rb') as fid:
      skips = pickle.load(fid)
  # create the output directory
  os.makedirs(flags.output_root, exist_ok=True)
  # now do the tracking.
  for s in seqns['eval']:
    print(f'Current sequence is:{s}')
    # are we skipping?
    if skips is not None:
      files = skips[s]
    else:
      files = fpseq[s]
    # create the tracker
    tracker = ourtracker.mytracker(flags,get_my_criterion(flags.distance_criteria))
    for f in files:
      # get the mask2former outputs
      with open(os.path.join(flags.m2f, str(s), str(f)+'.pkl'), 'rb') as fid:
        data = pickle.load(fid)
      if len(data.keys())>0:
        inputs = []
        for k, v in data.items():
          bbox = v['bbox']
          inputs.append([bbox[0],bbox[1],bbox[0]+bbox[2],bbox[1]+bbox[3], 1.])
        tracker.update(np.array(inputs), f)
    # call the tracker and track
    tracker(os.path.join(flags.output_root, f'{s}.txt'))
