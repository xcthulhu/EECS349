#!/usr/bin/env python

from os.path import exists
import sys
import glob
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from random import shuffle
import os

def touch(fname, times=None):
    with file(fname, 'a'):
        os.utime(fname, times)

def load_fraction(fn, frac=.1,dims=None) :
    "Loads a random fraction of vectors from a .npy file"
    try : 
        data = np.load(fn, mmap_mode='r')
        if dims : assert data.shape[1] == dims
        rows = data.shape[0]
        idx = np.arange(rows)
        np.random.shuffle(idx)
        return data[idx[:int(rows*frac)]]
    except :
        print "Could not load %s" % fn
        return None

if __name__ == "__main__":
    n_clusters = int(sys.argv[1])
    frac = float(sys.argv[2])
    dims = int(sys.argv[3])
    outfn = sys.argv[4]

    if exists(outfn) :
       if np.load(outfn).shape[1] == dims: 
          print outfn, "exists and has", dims, "dimension - exiting"
          touch(outfn)
          exit()

    # Get files
    if exists(sys.argv[5]) :
       fp = open(sys.argv[5])
       files = [l.strip() for l in fp.readlines()]
       fp.close()
    else : files = glob.glob(sys.argv[5])
    print "Loading %i files" % len(files)
    # Get data
    raw_data = [ d for d in map(lambda fn : 
                   load_fraction(fn, 
                                 frac=frac,
                                 dims=dims), 
                   files)
                 if d != None and d.shape[1] == dims ]
    try :
        data = np.vstack(raw_data)
    except :
        import code
	code.InteractiveConsole(locals=globals()).interact()
    #data = np.vstack(map(np.load,files))
    print "Loaded %i vectors from %i files" % (len(data), len(files))

    # Use MiniBatch KMeans to extract centers
    mbk = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters,
                          batch_size=45, n_init=10, max_no_improvement=10,
                          verbose=0)
    mbk.fit(data)
    print "Extracted %i clusters" % n_clusters

    # Save results
    np.save(outfn, mbk.cluster_centers_)
