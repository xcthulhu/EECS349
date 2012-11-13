#!/usr/bin/env python2.7
import glob
import sys
import numpy as np
from os.path import basename
from collections import defaultdict
from sklearn import svm

def uniq(lst):
   u = []
   d = defaultdict(bool)
   for x in lst :
      if not d[x] :
         d[x] = True
         u.append(x)
   return u

def file_classes(files):
   "Computes the classes for a list of files"
   file_classes = [ basename('_'.join(f.split('_')[:-1])) 
                    for f in files ]
   classes = uniq(file_classes)
   class_enum = dict(zip(classes,range(len(classes))))
   return np.array([class_enum[file_classes[i]]
                    for i in range(len(files))])

if __name__ == "__main__":
   files = glob.glob(sys.argv[1])
   classes = file_classes(files)
   data = np.array([np.load(f) for f in files])
   # FIXME: Do cross validation to gather statistics
   clf = svm.SVC()
   clf.fit(data,classes)
   pred = clf.predict(data)
   print "Correct:", np.sum(pred == classes) , '/', len(classes), ':', np.sum(pred == classes) * 1.0 / len(classes)
