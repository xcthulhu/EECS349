#!/usr/bin/env python

import glob
import sys
import os, errno
from random import shuffle

"""Takes a file glob and a directory and outputs k training-test pairs using cross validation"""

def mkdir_p(path):
    try: os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST \
           and os.path.isdir(path): pass
        else: raise

def chunks(lst, n):
    """Yield n successive chunks from l"""
    newn = int(len(lst) / n)
    for i in xrange(0, n-1):
        yield lst[i*newn:i*newn+newn]
    yield lst[n*newn-newn:]

def flatten(lst):
    """Flattens a list"""
    return [y for x in lst for y in x]

if __name__ == "__main__":
   k = int(sys.argv[1])
   # Get files and randomize
   files = glob.glob(sys.argv[2])
   shuffle(files)
   # Break files up into k folds
   folds = list(chunks(files,k))
   # Create destination directory
   destd = sys.argv[3]
   mkdir_p(destd)
   # Print all of the training-testing pairs to file
   for i in range(len(folds) - 1):
       train = open(os.path.join(destd,"%i-%i-train.txt" % (i,k)), 'w')
       train.writelines("%s\n" % l for f in folds[:i] + folds[i+1:]
                                   for l in f)
       train.close()
       test = open(os.path.join(destd,"%i-%i-test.txt" % (i,k)), 'w')
       test.writelines("%s\n" % l for l in folds[i])
       test.close() 
