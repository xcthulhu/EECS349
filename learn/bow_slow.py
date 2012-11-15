#!/usr/bin/env python
import glob
import sys
import numpy as np
import os
import mimetypes

def load_filenames(arg):
  "Loads filenames from a file or glob"
  if mimetypes.guess_type(arg)[0] == 'text/plain':
    fp = open(arg)
    for l in fp.readlines(): yield l.strip()
    fp.close()
  elif os.path.exists(arg): yield arg
  else : 
    for f in glob.glob(arg): yield f

def slowly_label_data(features, clusters):
  "Label data using O(n^2) time algorithm"
  from sklearn.metrics.pairwise import pairwise_distances
  return np.array(map(np.argmin, pairwise_distances(features, clusters)))

def mk_bow(features,label_fun,target_len,destfn):
  "Make a bag of words"
  if os.path.exists(destfn) and \
     len(np.load(destfn,mmap_mode='r')) == target_len :
     print "Already wrote %s, skipping" % destfn
     return
  labels = label_fun(features)
  # Compute a label histogram
  hist = np.bincount(labels,minlength=target_len)
  # Save to file
  np.save(destfn,hist)
  print "Wrote", destfn, "shape:", np.shape(hist)

if __name__ == "__main__":
  # Load clusters
  clusters = np.load(sys.argv[1])
  # Set up files
  files = load_filenames(sys.argv[2])

  # Use slow labeling
  label_fun = lambda f : slowly_label_data(f,clusters)

  # Make the Bags of Words
  for fn in files:
    features = np.load(fn)
    destfn = os.path.join(sys.argv[3],os.path.basename(fn))
    mk_bow(features,label_fun,len(clusters),destfn)
