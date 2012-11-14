#!/usr/bin/env python

import glob
import sys
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
import os
import mimetypes

def load_filenames(fn):
  "Loads filenames from a file"
  fp = open(fn)
  for l in fp.readlines():
    yield l.strip()
  fp.close()

if __name__ == "__main__":
  clusters = np.load(sys.argv[1])

  # Set up files
  if mimetypes.guess_type(sys.argv[2])[0] == 'text/plain':
    files = load_filenames(sys.argv[2])
  elif os.path.exists(sys.argv[2]): files = [sys.argv[2]]
  else : files = glob.glob(sys.argv[2])

  for fn in files:
    hogs = np.load(fn)
    dest = os.path.join(sys.argv[3],os.path.basename(fn))
    if os.path.exists(dest) and \
       len(np.load(dest,mmap_mode='r')) == len(clusters) :
       print "Already wrote %s, skipping" % dest
       continue
    # Compute a distance matrix, from it get HOG labels
    labels = np.array(map(np.argmax,
                          pairwise_distances(hogs, clusters)))
    # Compute a label histogram
    hist = np.bincount(labels,minlength=len(clusters))
    print "Wrote", fn, "shape:", np.shape(hist)
    # Save to file
    np.save(dest,hist)
