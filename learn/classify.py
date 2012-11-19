#!/usr/bin/env python2.7
import glob
import sys
import numpy as np
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import Scaler
from os.path import basename
from collections import defaultdict
from bow_slow import load_filenames
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def uniq(lst):
   u = []
   d = defaultdict(bool)
   for x in lst :
      if not d[x] :
         d[x] = True
         u.append(x)
   return u

def float_range(start,finish,step=.1):
   x = min(start,finish)
   while x <= max(start,finish) :
     yield x
     x += step

def class_dict(files):
   "Computes the classes for a list of files"
   file_classes = [ basename('_'.join(f.split('_')[:-1])) 
                     for f in files ]
   classes = uniq(file_classes)
   d0 = dict(zip(classes,range(len(classes))))
   d = {}
   for fn, cls in zip(files, file_classes):
       d[fn] = d0[cls]
   return d

def read_data(files,d,dims):
    data = [p for p in [(np.load(f),d[f]) for f in files]
              if p[0].shape[0] == dims ]
    return (np.vstack(map(lambda x: x[0], data)),
            np.array(map(lambda x: x[1], data)))

def test_classifier(train_data, test_data, clf, txt):
   clf.fit(train_data,train_classes)
   pred = clf.predict(test_data)
   return txt + "\t%f" % pred

if __name__ == "__main__":
   # Get Data
   train_files = glob.glob(sys.argv[1])
   test_files = glob.glob(sys.argv[2])
   dims = int(sys.argv[3])
   print "Computing classes... " ; sys.stdout.flush()
   d = class_dict(train_files+test_files)
   print len(uniq(d.values())), "classes computed"
   print "Reading %i training examples... " % len(train_files) ; sys.stdout.flush()
   train_data,train_classes = read_data(train_files,d,dims)
   print "done"
   print "Reading %i testing examples... " % len(test_files) ; sys.stdout.flush()
   test_data,test_classes = read_data(test_files,d,dims)
   print "done"
   # Rescale data
   sys.stdout.write("Rescaling to training data... ")
   scaler = Scaler()
   scaler.fit(train_data)  
   train_data = scaler.transform(train_data)
   test_data = scaler.transform(test_data)
   print "done"
   if train_data.shape[0] == train_classes.shape[0] :
      print "Training using %i vectors of dimension %i" % train_data.shape
   else :
      print >>sys.stderr, "Error in computing training classes", \
                           "- train_data.shape =", train_data.shape, \
                           "- train_classes.shape =", train_classes.shape
      exit()
   if test_data.shape[0] == test_data.shape[0] :
      print "Training using %i vectors of dimension %i" % test_data.shape
   else :
      print >>sys.stderr, "Error in computing testing classes", \
                           "- test_data.shape =", test_data.shape, \
                           "- test_classes.shape =", test_classes.shape
      exit()
   
   test_results = map(lambda p: test_classifier(test_data,train_data,p[0],p[1]),
                      [("SGD_hinge_l2",SGDClassifier(loss="hinge", penalty="l2")),
                       ("SGD_hinge_l1",SGDClassifier(loss="hinge", penalty="l1")),
                       ("SGD_hinge_elasticnet",SGDClassifier(loss="hinge", penalty="elasticnet"))])

   print "\n".join(test_results)
   #for C in costs:
   #  print "Cost:", C 
   #  clf = svm.SVC(C=C)
