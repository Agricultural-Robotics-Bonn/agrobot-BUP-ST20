# Agrobot-BUP-ST20 Dataset and Tracking and Evaluation Code

Please cite the paper
```
Weakly Labelled Spatial-Temporal Sweet Pepper Data: enabling higher quality detection, segmentation, and tracking.
Esra Guclu, Michael Halstead, Simon Denman, and Chris McCool
2025
```

# The BUP-ST20 dataset

ESRA to complete.

# The tracking and evaluation code.

First you need to clone the repository.

## Creating the virtual environment.

```cd agrobot-BUP-ST20```

```python3 -m venv yourname```

```. yourname/bin/activate```

```pip3 install -r requirements.txt```

To deactivate

```deactivate yourname```

## Installing ByteTrack - This has to happen for the repository to work!!

In the ```agrobot-BUP-ST20``` directory clone the ByteTrack repository.

```git clone git@github.com:ifzhang/ByteTrack.git```

add to your python path.
```export PYTHONPATH=${PYTHONPATH}:$/yourpath/agrobot-BUP-ST20/ByteTrack```

You do not need to install their requirements.txt in the virtual environment.
But you do need to do the following

```cd ByteTrack```

```python3 setup.py develop```

Now install the final libraries

```pip3 install cython; pip3 install 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'```

```pip3 install cython_bbox```

Finally, to run it with our tracking and evaluation you need to change some of the code in the ByteTrack repository.

In ```ByteTrack.yolox.tracker.matching``` change the following function

```def iou_distance(atracks, btracks)```

to

```def iou_distance(atracks, btracks, *args, **kwargs)```

## Running for ByteTrack and Our Tracker for MOT

Look in the ```run_example``` directory for examples of how to run different experiments on our tracker and bytetrack.

## Running the evaluation once txt files have been created

Look in the ```run_example``` directory for examples of how to run the evaluations after you have tracked the files for our tracker and bytetrack.

## The hyper-parameters and the repositories for the different state-of-the-art tracking techniques

Please note, the code in the public repositories belongs to their owners and we only provide the links to their code.
In our experiments we did not modify any code, apart from ByteTrack, and just varied hyper-parameters.

Below are the hyper-parameters for the full experiment.
Please note that some minor changes have been made to our tracker that might slightly alter the results from the paper.

| Method | Repository | Hyper-parameters |
| --- | --- | --- |
| Sort | [here](https://github.com/abewley/sort) | age=20, min hits=1, iou=0.3 |
| DeepSort | [here](https://github.com/nwojke/deep_sort) | cosine=0.3, nn budget=100, min confidence=0.5 nms max=0.5 |
| FairMOT | [here](https://github.com/ifzhang/FairMOT) | re-id=on, det=0.5 |
| ByteTrack IoU | [here](https://github.com/FoundationVision/ByteTrack) | det=0.5, mt=0.9, st=0.5, ut=0.7, track buffer=20 |
| ByteTrack DR | [here](https://github.com/FoundationVision/ByteTrack) + This repository | det=0.5, mt=1.0, st=1.0, ut=1.0, track buffer=10, radius=maximum |
| ByteTrack DRE-D | [here](https://github.com/FoundationVision/ByteTrack) + This repository | det=0.5, mt=1.0, st=1.0, ut=1.0, track buffer=10, beta=0.5, radius=maximum, delta=summation |
| ByteTrack DRE-S | [here](https://github.com/FoundationVision/ByteTrack) + This repository | det=0.5, mt=1.0, st=1.0, ut=1.0, track buffer=10, beta=0.5, radius=maximum, delta=maximum |
| StrongSort | [here](https://github.com/dyhBUPT/StrongSORT) | consine=0.4, nn budget=1, min confidence=0.5, nms max=0.5 |
| OCSort | [here](https://github.com/noahcao/OC_SORT) | det=0.7, iou=0.3, max age=20, min hits=1, delta=1, association function=iou, inertia=0.2, use bytetrack=True |
| CTVIS | [here](https://github.com/KainingYing/CTVIS) | lr=5e-5, all others default |
| OurTracker IoU | This repository | threshold=0.9, min tracks=5, keep running=10, use checks=True |
| OurTracker DR | This repository | threshold=1.0, min tracks=5, keep running=5, use checks=True, radius=minimum |
| OurTracker DRE-D | This repository | threshold=1.0, min tracks=10, keep running=2, radius=maximum, delta=maximum, beta=1.0 |
| M2F-VIS | [here](https://github.com/facebookresearch/Mask2Former) | lr=5e-5, all others default |
| VITA | [here](https://github.com/sukjunhwang/VITA) | lr=5e-5, all others default |
| PAg-NeRF | [here](https://github.com/Agricultural-Robotics-Bonn/pagnerf) | Default values |

Below are the hyper-parameters for Ablation study I - random skipping.

| Method | Hyper-parameters |
| --- | --- |
| ByteTrack IoU | det=0.5, mt=0.9, st=0.5, ut=0.7, track buffer=5 |
| ByteTrack DR | det=0.5, mt=1.0, st=1.0, ut=1.0, track buffer=5, radius=maximum |
| ByteTrack DRE-S | det=0.5, mt=1.0, st=1.0, ut=1.0, track buffer=1, beta=0.5 radius=maximum, delta=summation |
| ByteTrack DRE-D | det=0.5, mt=1.0, st=1.0, ut=1.0, track buffer=1, beta=0.5, radius=maximum, delta=summation |
| FairMOT | re-id=on, det=0.5 |
| OCSort | det=0.6, iou=0.3, max age=5, min hits=1, delta=2, association function=iou, inertia=0.2, use bytetrack=True |
| Our Tracker IoU | threshold=0.9, min tracks=2, keep running=10, use checks=True |
| Our Tracker DR | threshold=1.0, min tracks=2, keep running=10, use checks=True, radius=maximum |
| Our Tracker DRE-D | threshold=1.0, min tracks=5, keep running=10, use checks=True, radius=maximum, delta=summation, beta=1.0 |

Below are the hyper-parameters for Ablation Study I - low frame rates.
In 2f we list all the hyper-parameters selected, for 5f and 10f we only list them if they are different to 2f.

| Method | 2f | 5f | 10f |
| --- | --- | --- | --- |
| ByteTrack IoU | det=0.5, mt=0.9, st=0.5, ut=0.7, track buffer=10 | track buffer=30 | track buffer=30 |
| ByteTrack DR | det=0.5, mt=1.0, st=1.0, ut=1.0, track buffer=5, radius=maximum | track buffer=1 | track buffer=1 |
| ByteTrack DRE-S | det=0.5, mt=1.0, st=1.0, ut=1.0, track buffer=1, beta=0.5, radius=maximum, delta=summation | - | track buffer=30 |
| ByteTrack DRE-D | det=0.5, mt=1.0, st=1.0, ut=1.0, track buffer=5, beta=0.5, radius=maximum, delta=summation | track buffer=1 | track buffer=1 |
| FairMOT | re-id=on, det=0.5 | - | - |
| OCSort | det=0.6, iou=0.3, max age=10, min hits=1, delta=5, association function=iou, inertia=0.2, use bytetrack=True | inertia=0.1 | max age=20 |
| Our Tracker IoU | threshold=0.9, min tracks=2, keep running=10, use checks=True | min tracks=1 | min tracks=1 |
| Our Tracker DR | threshold=1.0, min tracks=2, keep running=10, use checks=True, radius=maximum | min tracks=1, keep running=1 | min tracks=1, keep running=1 |
| Our Tracker DRE-D | threshold=1.0, min tracks=5, keep running=10, use checks=True, radius=maximum, delta=summation | min tracks=1 | min tracks=1, keep running=1 |




## Other papers to cite.

For our tracker with dynamic radius.
```
@article{halstead2021crop,
  title={Crop agnostic monitoring driven by deep learning},
  author={Halstead, Michael and Ahmadi, Alireza and Smitt, Claus and Schmittmann, Oliver and McCool, Chris},
  journal={Frontiers in plant science},
  volume={12},
  pages={786702},
  year={2021},
  publisher={Frontiers Media SA}
}
```

For our IoU based tracker.
```
@Article{halstead2018fruit,
  author    = {Halstead, Michael and McCool, Christopher and Denman, Simon and Perez, Tristan and Fookes, Clinton},
  title     = {Fruit quantity and ripeness estimation using a robotic vision system},
  journal   = {IEEE Robotics and Automation Letters},
  year      = {2018},
  volume    = {3},
  number    = {4},
  pages     = {2995--3002},
  keywords  = {rank5},
  publisher = {IEEE},
}
```
