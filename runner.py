"""
  The main script to run either bytetrack or our tracker.
  If you want to run other trackers you will need to download them from their respective repositories listed in the readme.

  Created: MAH 20250626

"""

import argparse

from engine.tracking.trackers import base_creator

def parser():
  parser = argparse.ArgumentParser(description='Extracting command line arguments', add_help=True)

  # basic inputs required.
  # the eval sequences yaml - also mask2former sequences
  parser.add_argument('--yaml', action='store', required=True) # ../final_seq_info.yaml
  # for the mask2former images per sequence
  parser.add_argument('--image_yaml', action='store', required=True) # ../final_sequences.yaml )
  # mask2former pickle locations - you can use either depth filtered or standard.
  parser.add_argument('--m2f', action='store', required=True) # ../mask2former_depthfiltered )
  # get the directory to the images.
  parser.add_argument('--image_loc', action='store', required=True)
  # do we have a pickle file with the images being used - for skipping
  parser.add_argument('--skip_files', action='store', default=None)

  # output root location
  parser.add_argument('--output_root', action='store', required=True)

  # which tracker type are you using? default is our tracker.
  parser.add_argument('--usebytetrack', action='store_true')
  # for both bytetrack and our tracker you need to specify the distance criteria ('default', 'dr', 'dre_delta', 'dre_sigma')
  parser.add_argument('--distance_criteria', action='store', default='default')

  # here are the hyper-parameters for our tracker. Set up to be default (IoU) for the best results for the best results.
  parser.add_argument('--threshold', action='store', type=float, default=0.9)
  parser.add_argument('--min_tracks', action='store', type=int, default=5)
  parser.add_argument('--keep_running', action='store', type=int, default=10)
  parser.add_argument('--radius_ot', action='store', default='maximum') # for DR and DRE-D only: minimum (for DR) and maximum (for DRE-D)
  parser.add_argument('--delta_ot', action='store', default='maximum') # for DRE-D only: [default, maximum, summation]
  parser.add_argument('--usechecks', action='store', default='true') 
  parser.add_argument('--beta_ot', action='store', type=float, default=1.0) # for DRE-D only.

  # here are the hyper-parameters for bytetrack. Set up to be default (IoU) for the best results.
  parser.add_argument('--track_thresh', type=float, default=0.6)
  parser.add_argument('--det_thresh', type=float, default=0.5)
  parser.add_argument('--track_buffer', type=int, default=20) # 10 for DR and DRE-*
  parser.add_argument('--match_thresh', type=float, default=0.9) # 1.0 for DR and DRE-*
  parser.add_argument('--match_second', type=float, default=0.5) # 1.0 for DR and DRE-*
  parser.add_argument('--match_unconfirmed', type=float, default=0.7) # 1.0 for DR and DRE-*
  parser.add_argument('--mot20', dest="mot20", action="store_true")
  parser.add_argument('--beta_bt', type=float, default=0.5) # only for DRE-*
  parser.add_argument('--radius_bt', default='maximum') # ['minimum', 'maximum'] set to maximum for both DRE-* versions
  parser.add_argument('--delta_bt', default='maximum') # ['maximum', 'default', 'summation'] set to summation for DRE-D

  # return the parsed arguments
  return parser.parse_args()


# main function
if __name__ == "__main__":
  # get the input flags
  flags = parser()
  # do the tracking
  base_creator(flags)
