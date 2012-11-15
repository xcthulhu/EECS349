#!/usr/bin/env python
from pyflann import FLANN
import numpy as np
import sys
import pickle

if __name__ == "__main__":
   flann = FLANN()
   target_precision = float(sys.argv[1])
   params = flann.build_index(np.load(sys.argv[2]),
                              target_precision = target_precision,
                              log_level = "info")
   print "FLANN params: ", params
   # Save the FLANN
   flann.save_index(sys.argv[3])
   # Save the params
   p_output = open(sys.argv[4], 'wb')
   pickle.dump(params, p_output)
   p_output.close()
