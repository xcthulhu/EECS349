#!/usr/bin/env python

from os.path import exists
import sys
import glob
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from random import shuffle

def load_fraction(fn, frac=.1, shape=None) :
    "Loads a random fraction of vectors from a .npy file"
    try : 
        if shape :
            data = np.reshape(np.load(fn),shape)
        else :
            data = np.load(fn, mmap_mode='r')
        idx = np.arange(len(data))
        np.random.shuffle(idx)
        return data[idx[:int(len(data)*frac)]]
    except :
        print "Could not load %s" % fn
        return np.zeros(0)

if __name__ == "__main__":
    n_clusters = int(sys.argv[1])
    frac = float(sys.argv[2])
    shape = (-1,int(sys.argv[3]))
    outfn = sys.argv[4]

    # Get files
    if exists(sys.argv[5]) :
       fp = open(sys.argv[5])
       files = [l.strip() for l in fp.readlines()]
       fp.close()
    else : files = glob.glob(sys.argv[5])

    print "Loading %i files" % len(files)
    data = np.vstack(map(lambda fn : load_fraction(fn, frac=frac, shape=shape), 
                         files))
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
