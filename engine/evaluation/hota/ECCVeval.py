import time
import traceback
from multiprocessing.pool import Pool
from functools import partial
import os
from . import utils
from .utils import TrackEvalException
from . import _timing
from .metrics import Count

try:
    import tqdm
    TQDM_IMPORTED = True
except ImportError as _:
    TQDM_IMPORTED = False


class Evaluator:
    """Evaluator class for evaluating different metrics for different datasets"""

    @staticmethod
    def get_default_eval_config():
        """Returns the default config values for evaluation"""
        code_path = utils.get_code_path()
        default_config = {
            'USE_PARALLEL': False,
            'NUM_PARALLEL_CORES': 8,
            'BREAK_ON_ERROR': True,  # Raises exception and exits with error
            'RETURN_ON_ERROR': False,  # if not BREAK_ON_ERROR, then returns from function on error
            'LOG_ON_ERROR': os.path.join(code_path, 'error_log.txt'),  # if not None, save any errors into a log file.

            'PRINT_RESULTS': False,
            'PRINT_ONLY_COMBINED': False,
            'PRINT_CONFIG': False,
            'TIME_PROGRESS': False,
            'DISPLAY_LESS_PROGRESS': True,

            'OUTPUT_SUMMARY': False,
            'OUTPUT_EMPTY_CLASSES': True,  # If False, summary files are not output for classes with no detections
            'OUTPUT_DETAILED': False,
            'PLOT_CURVES': False,
        }
        return default_config

    def __init__(self, config=None):
        """Initialise the evaluator with a config file"""
        self.config = utils.init_config(config, self.get_default_eval_config(), 'Eval')
        # Only run timing analysis if not run in parallel.
        if self.config['TIME_PROGRESS'] and not self.config['USE_PARALLEL']:
            _timing.DO_TIMING = True
            if self.config['DISPLAY_LESS_PROGRESS']:
                _timing.DISPLAY_LESS_PROGRESS = True

    @_timing.time
    def evaluate(self, dataset_list, metrics_list, show_progressbar=False):
        """Evaluate a set of metrics on a set of datasets"""
        config = self.config
        metrics_list = metrics_list + [Count()]  # Count metrics are always run
        metric_names = utils.validate_metrics_list(metrics_list)
        dataset_names = [dataset.get_name() for dataset in dataset_list]
        # print( dataset_names ); sys.exit( 1 )
        output_res = {}
        output_msg = {}

        for dataset, dataset_name in zip(dataset_list, dataset_names):
            # Get dataset info about what to evaluate
            output_res[dataset_name] = {}
            output_msg[dataset_name] = {}
            tracker_list, seq_list, class_list = dataset.get_eval_info()
            # print('\nEvaluating %i tracker(s) on %i sequence(s) for %i class(es) on %s dataset using the following '
            #       'metrics: %s\n' % (len(tracker_list), len(seq_list), len(class_list), dataset_name,
            #                          ', '.join(metric_names)))

            # Evaluate each tracker
            for tracker in tracker_list:
                # print( tracker )
                curr_seq = os.path.splitext( tracker )[0]
                res = {}
                res = eval_sequence(curr_seq, dataset, tracker, class_list, metrics_list,
                                              metric_names)

                # # Output for returning from function
                output_res[dataset_name][curr_seq] = res
                output_msg[dataset_name][curr_seq] = 'Success'

            # trying to combine this shit!
            # Combine results over all sequences and then over all classes

            # collecting combined cls keys (cls averaged, det averaged, super classes)
            combined_cls_keys = []
            res = {}
            # combine sequences for each class
            for c_cls in class_list:
                res[c_cls] = {}
                for metric, metric_name in zip(metrics_list, metric_names):
                    curr_res = {}
                    for seq_key, seq_val in output_res[dataset_name].items():
                      curr_res[seq_key] = seq_val[c_cls][metric_name]
                    res[c_cls][metric_name] = metric.combine_sequences( curr_res )

            output_res[dataset_name]['COMBINED_SEQENCE'] = res
            output_msg[dataset_name]['COMBINED_SEQENCE'] = 'Success'
        return output_res, output_msg


@_timing.time
def eval_sequence(seq, dataset, tracker, class_list, metrics_list, metric_names):
    """Function for evaluating a single sequence"""
    raw_data = dataset.get_raw_seq_data(tracker, seq)
    seq_res = {}
    for cls in class_list:
        seq_res[cls] = {}
        data = dataset.get_preprocessed_seq_data(raw_data, cls)
        for metric, met_name in zip(metrics_list, metric_names):
            seq_res[cls][met_name] = metric.eval_sequence(data)
    return seq_res
