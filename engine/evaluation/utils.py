"""
  Some little helper files

  created: MAH 20240603
"""

def get_unique_frames( gt, preds ):
  frames = []
  with open( gt, 'r' ) as fid:
    lines = fid.readlines()
    for l in lines:
      frames.append( l.split( ',' )[0] )
  with open( preds, 'r' ) as fid:
    lines = fid.readlines()
    for l in lines:
      frames.append( l.split( ',' )[0] )
  return sorted( list( set( frames ) ) )

# default_mot_challenge_2d_box_config = {
#         'display_name_in_plot': '', ## to set equal to 'output_file_name' in 'default_eval_config'
#         'total_frame_num': '',## to set or calculate total frames in gt_file
#         'GT_file': '',## to set gt_file location
#         'TRACKER_FILE': '',## to set predicted tracker file location
#         'OUTPUT_FOLDER': '',## to set where to store evaluation results
#         # Where to save eval results (if None, same as TRACKERS_FOLDER)
#         'CLASSES_TO_EVAL': ['pepper'],  # Valid: ['pedestrian'] ##
#         'INPUT_AS_ZIP': False,  # Whether tracker input files are zipped
#         'PRINT_CONFIG': False,  # Whether to print current config
#         'DO_PREPROC': False,  # Whether to perform preprocessing (never done for MOT15)
#     }

default_config = {
    'GT_FOLDER': '', #os.path.join(code_path, 'data/gt/mot_challenge/'),  # Location of GT data
    'TRACKERS_FOLDER': '', #os.path.join(code_path, 'data/trackers/mot_challenge/'),  # Trackers location
    'OUTPUT_FOLDER': None,  # Where to save eval results (if None, same as TRACKERS_FOLDER)
    'TRACKERS_TO_EVAL': None,  # Filenames of trackers to eval (if None, all in folder)
    'CLASSES_TO_EVAL': ['pepper'],  # Valid: ['pedestrian']
    'BENCHMARK': '', #'MOT17',  # Valid: 'MOT17', 'MOT16', 'MOT20', 'MOT15'
    'SPLIT_TO_EVAL': 'all', #'train',  # Valid: 'train', 'test', 'all'
    'INPUT_AS_ZIP': False,  # Whether tracker input files are zipped
    'PRINT_CONFIG': False,  # Whether to print current config
    'DO_PREPROC': False,  # Whether to perform preprocessing (never done for MOT15)
    'TRACKER_SUB_FOLDER': '', #'data',  # Tracker files are in TRACKER_FOLDER/tracker_name/TRACKER_SUB_FOLDER
    'OUTPUT_SUB_FOLDER': '',  # Output files are saved in OUTPUT_FOLDER/tracker_name/OUTPUT_SUB_FOLDER
    'TRACKER_DISPLAY_NAMES': None,  # Names of trackers to display, if None: TRACKERS_TO_EVAL
    'SEQMAP_FOLDER': None,  # Where seqmaps are found (if None, GT_FOLDER/seqmaps)
    'SEQMAP_FILE': None,  # Directly specify seqmap file (if none use seqmap_folder/benchmark-split_to_eval)
    'SEQ_INFO': None,  # If not None, directly specify sequences to eval and their number of timesteps
    'GT_LOC_FORMAT': '{gt_folder}/{seq}/gt.txt',  # '{gt_folder}/{seq}/gt/gt.txt'
    'SKIP_SPLIT_FOL': True,  # If False, data is in GT_FOLDER/BENCHMARK-SPLIT_TO_EVAL/ and in
                              # TRACKERS_FOLDER/BENCHMARK-SPLIT_TO_EVAL/tracker/
                              # If True, then the middle 'benchmark-split' folder is skipped for both.
}
