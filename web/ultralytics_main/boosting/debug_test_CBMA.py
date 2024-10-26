# Ultralytics YOLO 🚀, AGPL-3.0 license

import contextlib
import csv
import urllib
from copy import copy
from pathlib import Path

import cv2
import numpy as np
import pytest
import torch
import yaml
from PIL import Image

from tests import CFG, MODEL, SOURCE, SOURCES_LIST, TMP
from ultralytics import RTDETR, YOLO
from ultralytics.cfg import MODELS, TASK2DATA, TASKS
from ultralytics.data.build import load_inference_source
from ultralytics.utils import (
    ASSETS,
    DEFAULT_CFG,
    DEFAULT_CFG_PATH,
    LOGGER,
    ONLINE,
    ROOT,
    WEIGHTS_DIR,
    WINDOWS,
    checks,
    is_dir_writeable,
    is_github_action_running,
)
from ultralytics.utils.downloads import download
from ultralytics.utils.torch_utils import TORCH_1_9

IS_TMP_WRITEABLE = is_dir_writeable(TMP)  # WARNING: must be run once tests start as TMP does not exist on tests/init
# ultralytics/cfg/models/v8/yolov8.yaml boosting/yolov8_cbam.yaml
CFG = 'boosting/yolov8_cbam.yaml'
SOURCE = ROOT / 'assets/bus.jpg'



def test_model_forward():
    """Test the forward pass of the YOLO model."""
    model = YOLO(CFG)
    model(SOURCE)