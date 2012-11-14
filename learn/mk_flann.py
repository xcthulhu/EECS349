#!/usr/bin/env python
from pyflann import FLANN
import numpy as np
import sys

if __name__ == "__main__":
   flann = FLANN()
   print flann.build_index(np.load(sys.argv[1]),
                           target_precision = 0.9,
                           log_level = "info")
   flann.save_index(sys.argv[2])
