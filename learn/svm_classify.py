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

def file_classes(train_files, test_files):
   "Computes the classes for a list of files"
   train_classes = [ basename('_'.join(f.split('_')[:-1])) 
                     for f in train_files ]
   test_classes = [ basename('_'.join(f.split('_')[:-1])) 
                    for f in test_files ]
   classes = uniq(train_classes + test_classes)
   class_enum = dict(zip(classes,range(len(classes))))
   return (np.array([class_enum[cls]
                     for cls in train_classes]),
           np.array([class_enum[cls]
                     for cls in test_classes]))

if __name__ == "__main__":
   train_files = glob.glob(sys.argv[1])
   test_files = glob.glob(sys.argv[2])
   train_classes, test_classes = file_classes(train_files,test_files)
   costs = map(float,sys.argv[3:])
   train_data = np.array([np.load(f) for f in train_files])
   #test_data = np.array([np.load(f) for f in test_files])
   test_data = train_data
   for C in costs:
     clf = svm.SVC(C=C)
     print train_data.shape, train_classes.shape
     clf.fit(train_data,train_classes)
     pred = clf.predict(test_data)
     print "Cost:", C, "Correct:", np.sum(pred == test_classes) , '/', len(test_classes), '=', np.mean(pred == test_classes) 
