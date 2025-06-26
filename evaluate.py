"""
  Evaluate a set of txt files.

  Needs:
    The full set of txt files for all sequences in the evaluation sets.
    The appropriate ground truth (check if skipping frames)
    The location to save to

  Created: MAH 20250626
"""

import argparse
import motmetrics as mm
import numpy as np
import os

from engine.evaluation.utils import get_unique_frames
from engine.evaluation.mota.evaluation import ECCV_Evaluator
import engine.evaluation.hota.ECCVeval as ome
import engine.evaluation.hota.datasets as omd
import engine.evaluation.hota.metrics as omm
from engine.evaluation.utils import default_config

# check the gt vs the preds
def check_inputs(pt_dir, gt_dir):
  missing = []
  dirs = sorted(os.listdir(gt_dir))
  for d in dirs:
    p = os.path.join(pt_dir, f'{d}.txt')
    if not os.path.isfile(p):
      missing.append(d)
  return missing

def get_info(pt_dir, gt_dir):
  dirs = sorted(os.listdir(gt_dir))
  dit = {}
  for d in dirs:
    # get the files
    p = os.path.join(pt_dir, f'{d}.txt')
    g = os.path.join(gt_dir, d, 'gt.txt')
    uf = get_unique_frames(g, p)
    dit[d] = uf
  return dit

def calculate_mota_etc(pt_dir, gt_dir):
    # for the HOTA metric
    default_eval_config = ome.Evaluator.get_default_eval_config()
    default_metrics_config = {'METRICS': ['HOTA'], 'THRESHOLD': 0.5}
    metrics_list = [omm.HOTA(default_metrics_config)]
    # for the other metrics
    metrics = mm.metrics.motchallenge_metrics
    # get the gt files to evaluate against
    dirs = sorted(os.listdir(gt_dir))
    accs, seqn_names = [], []
    # iterate over the directories
    for d in dirs:
      # get the sequence name
      seqn_names.append(d)
      # get the prediction file
      p = os.path.join(pt_dir, f'{d}.txt')
      # create the evaluator for the other metrics
      evaluator = ECCV_Evaluator(gt_dir, d, 'mot')
      accs.append(evaluator.eval_file(p))
    # calculate the other metrics
    summary = ECCV_Evaluator.get_summary(accs, seqn_names, metrics)
    mh = mm.metrics.create()
    strsummary = mm.io.render_summary(
      summary,
      formatters=mh.formatters,
      namemap=mm.io.motchallenge_metric_names
    )
    print(strsummary)
    return summary.iloc[-1]

def calculate_hota(pt_dir, gt_dir, info):
  default_config['GT_FOLDER'] = gt_dir
  default_config['TRACKERS_FOLDER'] = pt_dir
  default_config['SEQ_INFO'] = info
  default_eval_config = ome.Evaluator.get_default_eval_config()
  default_metrics_config = {'METRICS': ['HOTA'], 'THRESHOLD': 0.5}
  metrics_list = [omm.HOTA(default_metrics_config)]
  hota_evaluator = ome.Evaluator(default_eval_config)
  dataset_list = [omd.ECCVChallenge2DBox(default_config)]
  output_res, output_msg = hota_evaluator.evaluate(dataset_list, metrics_list, show_progressbar=False)
  print( 'sequence, HOTA(0)')
  for k, v in output_res['ECCVChallenge2DBox'].items():
    print(k, v['pepper']['HOTA']['HOTA(0)'])
  return output_res['ECCVChallenge2DBox']['COMBINED_SEQENCE']['pepper']['HOTA']['HOTA(0)']

def main(pt_dir, gt_dir, res_dir, info):
  mota = calculate_mota_etc(pt_dir, gt_dir)
  hota = calculate_hota(pt_dir, gt_dir, info)

  os.makedirs(res_dir, exist_ok=True)
  with open(os.path.join(res_dir, "scores.txt"), "w") as text_file:
    for k in mota.keys():
      text_file.write(f'{k}: {mota[k]} \n')
    text_file.write(f'hota: {hota} \n')


if __name__ == '__main__':
  #%% Parse arguments
  parser = argparse.ArgumentParser("./evaluate.py")
  parser.add_argument("--prediction", "-p",
                    help="Path to dataset root, where listdir will find p1,p2,p3,etc.")
  parser.add_argument("--ground_truth", "-g",
                    help="Path to dataset root, where listdir will find p1,p2,p3,etc.")
  parser.add_argument("--results", "-r",
                    help="Path to some folder")
  parser.add_argument( "--isdirectory", action='store_true', help='Is this a directory or a single file.' )
  args = parser.parse_args()

  # check to make sure all sequences and ground truth are the same.
  missing = check_inputs(args.prediction, args.ground_truth)
  if len(missing) == 0:
    info = get_info(args.prediction, args.ground_truth)
    main(args.prediction, args.ground_truth, args.results, info)
  else:
    print('You are misssing the following sequences:')
    for m in missing:
      print(m)
