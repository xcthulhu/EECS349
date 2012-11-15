#!/usr/bin/env python

import glob
import sys
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
import os
import mimetypes
from bow_slow import load_filenames, mk_bow

def load_flann(clusters, flannfn, paramsfn):
  "Loads the flann file and its parameters"
  from pyflann import FLANN
  import pickle
  flann = FLANN()
  flann.load_index(flannfn,clusters)
  params_p = open(paramsfn,'rb')
  params = pickle.load(params_p)
  params_p.close()
  return flann,params

def flann_label_data(features, flann, params):
  "Uses a flann object to label feature data"
  labels, _ = flann.nn_index(features,1,checks=params["checks"])
  return labels

if __name__ == "__main__":
  # Load clusters
  clusters = np.load(sys.argv[1])
  # Load flann
  flann,params = load_flann(clusters, sys.argv[2], sys.argv[3])
  # Set up files
  files = load_filenames(sys.argv[4])
  # Use slow labeling
  label_fun = lambda f : flann_label_data(f,flann,params)
  # Make the Bags of Words
  for fn in files:
    features = np.load(fn)
    destfn = os.path.join(sys.argv[5],os.path.basename(fn))
    mk_bow(features,label_fun,len(clusters),destfn)
