# Agrobot-BUP-ST20 Dataset and Tracking and Evaluation Code

Please cite the paper
```
Weakly Labelled Spatial-Temporal Sweet Pepper Data: enabling higher quality detection, segmentation, and tracking.
Esra Guclu, Michael Halstead, Simon Denman, and Chris McCool
2025
```

# The BUP-ST20 dataset

# The tracking and evaluation code.

## Creating the virtual environment.

```cd agrobot-BUP-ST20```

```python3 -m venv yourname```

```. yourname/bin/activate```

```pip3 install -r requirements.txt```

To deactivate

```deactivate yourname```

## Installing ByteTrack

In the ```agrobot-BUP-ST20``` directory clone the ByteTrack repository.

```git clone git@github.com:ifzhang/ByteTrack.git```

add to your python path.
```export PYTHONPATH=${PYTHONPATH}:$/yourpath/agrobot-BUP-ST20/ByteTrack```

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



## The hyper-parameters for the different tracking techniques
