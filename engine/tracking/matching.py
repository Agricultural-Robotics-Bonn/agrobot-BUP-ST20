"""
  Our matching schemes for ByteTrack.

  Created: MAH 20240605

  Modified: MAH 20250626
"""
import numpy as np
import sys

from ByteTrack.yolox.tracker.matching import *

"""
  Matching based on the dynamic radius.

  atracks = previous predictions
  btracks = current predictions
"""
def dynamicradius_distance(atracks, btracks, *args, radius='minimum', **kwargs):

  atlbrs = [track.tlbr for track in atracks]
  btlbrs = [track.tlbr for track in btracks]

  atlbrs = np.array(atlbrs)
  btlbrs = np.array(btlbrs)

  distance_dynamic_radius = np.zeros((atlbrs.shape[0], btlbrs.shape[0]), dtype=float)
  if distance_dynamic_radius.size == 0:
      return 1 - distance_dynamic_radius

  w_a = atlbrs[:,2] - atlbrs[:,0]
  h_a = atlbrs[:,3] - atlbrs[:,1]
  w_b = btlbrs[:,2] - btlbrs[:,0]
  h_b = btlbrs[:,3] - btlbrs[:,1]
  center_a = atlbrs[:,:2]
  center_a[:, 0] = atlbrs[:,0] + 0.5 * w_a
  center_a[:, 1] = atlbrs[:,1] + 0.5 * h_a
  center_b = btlbrs[:,:2]
  center_b[:, 0] = btlbrs[:,0] + 0.5 * w_b
  center_b[:, 1] = btlbrs[:,1] + 0.5 * h_b

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

"""
  Matching based on the elipse dynamically from the deltas of the tracklets.

  atracks = previous predictions
  btracks = current predictions
  alpha, beta = scaling of the radius denominator
  radius = what radius to use, ['minimum', 'maximum']
  delta = are we using the radius or just the delta ['maximum', 'default']
"""
def dynamicelipse_distance_delta(atracks, btracks, alpha=1.0, beta=1.0, radius='minimum', delta='maximum'):
  # get the bounding boxes
  atlbrs = [track.tlbr for track in atracks]
  btlbrs = [track.tlbr for track in btracks]

  atlbrs = np.array(atlbrs)
  btlbrs = np.array(btlbrs)

  # set up the default distance matrix
  distance_dynamic_elipse = np.zeros((atlbrs.shape[0], btlbrs.shape[0]), dtype=float)
  if distance_dynamic_elipse.size == 0:
      return 1 - distance_dynamic_elipse

  # get the center locations
  w_a = atlbrs[:,2] - atlbrs[:,0]
  h_a = atlbrs[:,3] - atlbrs[:,1]
  w_b = btlbrs[:,2] - btlbrs[:,0]
  h_b = btlbrs[:,3] - btlbrs[:,1]
  # get the minimum diameter for the deltas
  if radius == 'minimum':
    radius_a = np.minimum(w_a, h_a)
  elif radius == 'maximum':
    radius_a = np.maximum(w_a, h_a)
  else:
    assert False, f"Your radius {radius} is not included in this function"

  # get the center locations
  center_a = atlbrs[:,:2]
  center_a[:, 0] = atlbrs[:,0] + 0.5 * w_a
  center_a[:, 1] = atlbrs[:,1] + 0.5 * h_a
  center_b = btlbrs[:,:2]
  center_b[:, 0] = btlbrs[:,0] + 0.5 * w_b
  center_b[:, 1] = btlbrs[:,1] + 0.5 * h_b
  # get the deltas
  delta_x, delta_y = [], []
  for j, t in enumerate(atracks):
    xp = t.pos_x
    yp = t.pos_y
    dx,dy = 0,0
    for i in range(len(xp)-1):
      dx += np.abs(xp[i]-xp[i+1])
      dy += np.abs(yp[i]-yp[i+1])
    if delta == 'maximum':
      delta_x.append(np.maximum(radius_a[j], dx/float(len(xp)-1)))
      delta_y.append(np.maximum(radius_a[j], dy/float(len(yp)-1)))
    elif delta == 'default':
      delta_x.append(dx/float(len(xp)-1))
      delta_y.append(dy/float(len(yp)-1))
    elif delta == 'summation':
      delta_x.append(radius_a[j]+dx/float(len(xp)-1))
      delta_y.append(radius_a[j]+dy/float(len(yp)-1))
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


"""
  Calculate the eliplse based on the second order statistics from the kalman filter

  atracks: previous tracklets
  btracks: current tracklets
  alpha, beta: scaling of the radius denominator - not used in our experiments so default is 1.0
  radius: what radius to use, ['minimum', 'maximum']
  delta: are we using the radius or just the covariance ['maximum', 'default']

"""
def dynamicelipse_distance_sigma(atracks, btracks, alpha=1.0, beta=1.0, radius='minimum', delta='default'):
    # get the bounding boxes
    atlbrs = [track.tlbr for track in atracks]
    btlbrs = [track.tlbr for track in btracks]

    atlbrs = np.array(atlbrs)
    btlbrs = np.array(btlbrs)

    # get the covariances
    acov = [[np.sqrt(t.covariance[0,0]),np.sqrt(t.covariance[1,1])] for t in atracks]

    # set up the default distance matrix
    distance_dynamic_elipse = np.zeros((atlbrs.shape[0], btlbrs.shape[0]), dtype=float)
    if distance_dynamic_elipse.size == 0:
        return 1 - distance_dynamic_elipse

    # get the center locations
    w_a = atlbrs[:,2] - atlbrs[:,0]
    h_a = atlbrs[:,3] - atlbrs[:,1]
    w_b = btlbrs[:,2] - btlbrs[:,0]
    h_b = btlbrs[:,3] - btlbrs[:,1]
    # get the minimum diameter for the deltas
    if radius == 'minimum':
      radius_a = np.minimum(w_a, h_a)
    elif radius == 'maximum':
      radius_a = np.maximum(w_a, h_a)
    else:
      assert False, f"Your radius {radius} is not included in this function"
    # get the center locations
    center_a = atlbrs[:,:2]
    center_a[:, 0] = atlbrs[:,0] + 0.5 * w_a
    center_a[:, 1] = atlbrs[:,1] + 0.5 * h_a
    center_b = btlbrs[:,:2]
    center_b[:, 0] = btlbrs[:,0] + 0.5 * w_b
    center_b[:, 1] = btlbrs[:,1] + 0.5 * h_b
    # go through the covariances and make them equal to the radius if they are smaller than the radius
    if delta == 'maximum':
      for i in range(len(acov)):
        acov[i][0] = np.maximum(radius_a[i], acov[i][0])
        acov[i][1] = np.maximum(radius_a[i], acov[i][1])
    elif delta == 'default':
      pass
    elif delta == 'summation':
      for i in range(len(acov)):
        acov[i][0] = radius_a[i]+acov[i][0]
        acov[i][1] = radius_a[i]+acov[i][1]
    else:
      assert False, "Your delta parameter {delta} is not included in this function"

    #((x-h)**2)/r_x**2 + ((y-k)**2)/r_y**2 <= 1 if it's within the bounds.
    # from https://math.stackexchange.com/questions/76457/check-if-a-point-is-within-an-ellipse
    # (h,k) center of the elpise
    # (x,y) new point
    # r_x, r_y two radius
    for i in range(len(center_a)):
        for j in range(len(center_b)):
            distance_dynamic_elipse[i,j] = ((center_b[j,0]-center_a[i,0])**2)/(((beta*acov[i][0])**2)*alpha)+((center_b[j,1]-center_a[i,1])**2)/(((beta*acov[i][1])**2)*alpha)

    return distance_dynamic_elipse
