"""
  This is the original tracking algorithm from the two publications

  @article{halstead2018fruit,
  title={Fruit quantity and ripeness estimation using a robotic vision system},
  author={Halstead, Michael and McCool, Christopher and Denman, Simon and Perez, Tristan and Fookes, Clinton},
  journal={IEEE robotics and automation LETTERS},
  volume={3},
  number={4},
  pages={2995--3002},
  year={2018},
  publisher={IEEE}
  }

  And

  @article{halstead2021crop,
  title={Crop agnostic monitoring driven by deep learning},
  author={Halstead, Michael and Ahmadi, Alireza and Smitt, Claus and Schmittmann, Oliver and McCool, Chris},
  journal={Frontiers in plant science},
  volume={12},
  pages={786702},
  year={2021},
  publisher={Frontiers Media SA}
  }

  It's a basic tracker that is similar to bytetrack but without the second or unconfirmed matching.
  Has two basic matching types, iou, dr

  Does it based on the bounding box, not the segmentation, so the center of the bounding box is used for the dynamic radius.

  Created: MAH 20240705

  Modified: MAH 20250626
"""

import numpy as np

from cython_bbox import bbox_overlaps as bbox_ious

from ByteTrack.yolox.tracker import matching

def iou_distance(t, p, *args, **kwargs):
  ious = np.zeros((len(t), len(p)), dtype=np.float)
  if ious.size == 0:
      return ious

  ious = bbox_ious(
      np.ascontiguousarray(t, dtype=np.float),
      np.ascontiguousarray(p, dtype=np.float)
  )

  # return the cost matrix
  return 1 - ious


def dr_distance(t, p, *args, radius='minimum', **kwargs):
  distance_dynamic_radius = np.zeros((t.shape[0], p.shape[0]), dtype=float)
  if distance_dynamic_radius.size == 0:
      return 1 - distance_dynamic_radius
  w_a = t[:,2] - t[:,0]
  h_a = t[:,3] - t[:,1]
  w_b = p[:,2] - p[:,0]
  h_b = p[:,3] - p[:,1]
  center_a = t[:,:2]
  center_a[:, 0] = t[:,0] + 0.5 * w_a
  center_a[:, 1] = t[:,1] + 0.5 * h_a
  center_b = p[:,:2]
  center_b[:, 0] = p[:,0] + 0.5 * w_b
  center_b[:, 1] = p[:,1] + 0.5 * h_b

  for i in range(len(center_a)):
      for j in range(len(center_b)):
          distance_dynamic_radius[i,j] = np.sqrt(np.sum(np.square(center_a[i] - center_b[j])))
  if radius == 'maximum':
    radius_a = np.maximum(w_a, h_a)
  elif radius == 'minimum':
    radius_a = np.minimum(w_a, h_a)
  else:
    assert False, f"Your radius {radius} is not included in this function"

  radius_a = np.expand_dims(radius_a, axis=-1)
  cost_matrix = distance_dynamic_radius/radius_a

  return cost_matrix

def dre_delta(t, p, dx, dy, alpha=1.0, beta=1.0, radius='minimum', delta='summation'):
  # set up the default distance matrix
  distance_dynamic_elipse = np.zeros((t.shape[0], p.shape[0]), dtype=float)
  if distance_dynamic_elipse.size == 0:
      return 1 - distance_dynamic_elipse

  # get the center locations
  w_a = t[:,2] - t[:,0]
  h_a = t[:,3] - t[:,1]
  w_b = p[:,2] - p[:,0]
  h_b = p[:,3] - p[:,1]
  # get the minimum diameter for the deltas
  if radius == 'minimum':
    radius_a = np.minimum(w_a, h_a)
  elif radius == 'maximum':
    radius_a = np.maximum(w_a, h_a)
  else:
    assert False, f"Your radius {radius} is not included in this function"

  # get the center locations
  center_a = t[:,:2]
  center_a[:, 0] = t[:,0] + 0.5 * w_a
  center_a[:, 1] = t[:,1] + 0.5 * h_a
  center_b = p[:,:2]
  center_b[:, 0] = p[:,0] + 0.5 * w_b
  center_b[:, 1] = p[:,1] + 0.5 * h_b
  # get the deltas
  delta_x, delta_y = [], []
  for i in range(t.shape[0]):
    x = np.mean(np.abs(np.diff(dx[i])))
    y = np.mean(np.abs(np.diff(dy[i])))
    if delta == 'maximum':
      delta_x.append(np.maximum(radius_a[i], x))
      delta_y.append(np.maximum(radius_a[i], y))
    elif delta == 'default':
      delta_x.append(x)
      delta_y.append(y)
    elif delta == 'summation':
      delta_x.append(radius_a[i]+x)
      delta_y.append(radius_a[i]+y)
    else:
      assert False, "Your delta parameter {delta} is not included in this function"

  #((x-h)**2)/r_x**2 + ((y-k)**2)/r_y**2 <= 1 if it's within the bounds.
  # from https://math.stackexchange.com/questions/76457/check-if-a-point-is-within-an-ellipse
  # (h,k) center of the elpise
  # (x,y) new point
  # r_x, r_y two radius
  for i in range(len(center_a)):
      for j in range(len(center_b)):
          distance_dynamic_elipse[i,j] = ((center_b[j,0]-center_a[i,0])**2)/(((beta*delta_x[i])**2)*alpha)+((center_b[j,1]-center_a[i,1])**2)/(((beta*delta_y[i])**2)*alpha)

  return distance_dynamic_elipse


class tracklet():
  def __init__(self, bbox, score, id, image_name, keep_running=3):
    self.bboxs = []
    self.pos_x = []
    self.pos_y = []
    self.scores = []
    self.checks = []
    self.id = id
    self.running = True
    self.image_names = []
    self.keep_running = keep_running

    self.update(image_name, bbox, score)

  def update(self, image_name, bbox=None, score=None):
    if bbox is not None:
      self.bboxs.append(bbox)
      self.scores.append(score)
      self.image_names.append(image_name)
      self.checks.append(True)
      # get the shape of the bbox to start with as the delta
      if len(self.pos_x) == 0:
        self.pos_x = [bbox[0], bbox[2]]
        self.pos_y = [bbox[1], bbox[3]]
      else:
        self.pos_x.insert(0, bbox[0])
        self.pos_y.insert(0, bbox[1])
      if len(self.pos_x) > self.keep_running:
        self.pos_x.pop()
        self.pos_y.pop()
    else:
      self.bboxs.append(self.bboxs[-1])
      self.scores.append(self.scores[-1])
      self.checks.append(False)
      self.image_names.append(image_name)
      if len(self.checks) > self.keep_running:
        self.running = any(self.checks[-self.keep_running:])

  def hasfile(self, fname):
    return fname in self.image_names

  def istracklet(self, min_tracks):
    return sum(self.checks) > min_tracks

class mytracker():
  def __init__(self, args, criteria):
    self.args = args
    self.threshold = args.threshold
    self.min_tracks = args.min_tracks
    self.keep_running = args.keep_running
    self.tracklet_lib = list()
    self.id = 0
    self.criterion = criteria
    self.images = []


  def update(self, output_results, image_name):
    # store the image name
    self.images.append(image_name)
    # get the bounding boxes and the scores
    bboxs = output_results[:,:4]
    scores = output_results[:,4]

    # do we have any tracklets?
    if len(self.tracklet_lib) == 0:
      self.assign_new_tracks(bboxs, scores, image_name)
    else:
      self.investigate_tracks(bboxs, scores, image_name)

  def assign_new_tracks(self, bboxs, scores, image_name):
    for b, s in zip(bboxs, scores):
      self.tracklet_lib.append(tracklet(b, s, self.id, image_name))
      self.id += 1

  def investigate_tracks(self, bboxs, scores, image_name):
    # get the existing tracks
    running_tracks = []
    removed_tracks = []
    t_bboxs, delta_x, delta_y = [], [], []
    for t in self.tracklet_lib:
      if t.running:
        running_tracks.append(t)
        t_bboxs.append(t.bboxs[-1])
        delta_x.append(t.pos_x)
        delta_y.append(t.pos_y)
      else:
        removed_tracks.append(t)
    t_bboxs = np.array(t_bboxs) # tracked bounding boxes
    p_bboxs = np.array(bboxs)   # predicted bounding boxes
    # calculate the metrics between the boxes
    dists = self.criterion(t_bboxs, p_bboxs, delta_x, delta_y, alpha=1.0, beta=self.args.beta_ot, radius=self.args.radius_ot, delta=self.args.delta_ot)
    matches, u_track, u_detection = matching.linear_assignment(dists, thresh=self.threshold)
    # sort the matches
    for itracked, idet in matches:
      running_tracks[itracked].update(image_name, bbox=bboxs[idet], score=scores[idet])
    # get the unmatched tracks
    for i in u_track:
      running_tracks[i].update(image_name)
    # concatenate the running and removed tracks
    self.tracklet_lib = running_tracks + removed_tracks
    # add the new tracklets to the library
    o_bboxs = []
    o_scores = []
    for i in u_detection:
      o_bboxs.append(bboxs[i])
      o_scores.append(scores[i])
    if len(o_bboxs) > 0:
      self.assign_new_tracks(np.array( o_bboxs ), np.array( o_scores ), image_name)

  def __call__(self, txt):
    # get actual tracks
    actual_tracks = []
    for t in self.tracklet_lib:
      if t.istracklet(self.min_tracks):
        actual_tracks.append(t)
    # create the text file
    with open(txt, 'w') as fid:
      for fname in self.images:
        for t in actual_tracks:
          if t.hasfile(fname):
            i = t.image_names.index(fname)
            if self.args.usechecks == 'true':
              if t.checks[i]:
                bb = t.bboxs[i]
                score = t.scores[i]
                fid.write( f'{fname},{t.id},{bb[0]},{bb[1]},{np.abs(bb[2]-bb[0])},{np.abs(bb[3]-bb[1])},{score}\n' )
            elif self.args.usechecks == 'false':
              bb = t.bboxs[i]
              score = t.scores[i]
              fid.write( f'{fname},{t.id},{bb[0]},{bb[1]},{np.abs(bb[2]-bb[0])},{np.abs(bb[3]-bb[1])},{score}\n' )
            else:
              assert False, f"The use checks argument {self.args.usechecks} is not appropriate."
