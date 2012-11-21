#!/usr/bin/env python2.7
import glob
import sys
import numpy as np
#from sklearn import svm
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
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

def test_classifier(train_data, train_classes, test_data, test_classes, txt, clf):
   clf.fit(train_data,train_classes)
   pred = clf.predict(test_data)
   return txt + "\t%f" % np.mean(pred == test_classes)

def rescale(X):
    "Rescales a matrix X of vectors v"
    return (np.float64(X.T) / np.sum(X,1)).T

if __name__ == "__main__":
   # Get Data
   train_files = glob.glob(sys.argv[1])
   test_files = glob.glob(sys.argv[2])
   dims = int(sys.argv[3])
   print "Computing classes... " ; sys.stdout.flush()
   d = class_dict(train_files+test_files)
   print len(uniq(d.values())), "classes computed"
   print "Reading %i training examples... " % len(train_files), ; sys.stdout.flush()
   train_data,train_classes = read_data(train_files,d,dims)
   print "done"
   print "Reading %i testing examples... " % len(test_files), ; sys.stdout.flush()
   test_data,test_classes = read_data(test_files,d,dims)
   print "done"

   classifiers = [
                  ("SGD_hinge_l1",SGDClassifier(loss="hinge", penalty="l1")),
                  ("SGD_hinge_l2",SGDClassifier(loss="hinge", penalty="l2")),
                  ("SGD_hinge_elasticnet",SGDClassifier(loss="hinge", penalty="elasticnet")),
                  ("SGD_modified_huber_l1",SGDClassifier(loss="modified_huber", penalty="l1")),
                  ("SGD_modified_huber_l2",SGDClassifier(loss="modified_huber", penalty="l2")),
                  ("SGD_modified_huber_elasticnet",SGDClassifier(loss="modified_huber", penalty="elasticnet")),
                  ("SGD_log_l1",SGDClassifier(loss="log", penalty="l1")),
                  ("SGD_log_l2",SGDClassifier(loss="log", penalty="l2")),
                  ("SGD_log_elasticnet",SGDClassifier(loss="log", penalty="elasticnet")),
                  ("GaussianNB",GaussianNB()),
                  ("MultinomialNB",MultinomialNB()),
                  ("BernoulliNB",BernoulliNB()),
                  ("5NN-uniform",(KNeighborsClassifier(5,'uniform')))
                 ]

   test_results1 = map(lambda p: test_classifier(train_data,train_classes,test_data,test_classes,p[0],p[1]),
                       classifiers)
   out1 = open(sys.argv[4],'w')
   out1.write("\n".join(test_results1))
   out1.close()
   # Rescale data
   print "Rescaling to training data...", ; sys.stdout.flush()
   train_data_scale = rescale(train_data)
   test_data_scale = rescale(test_data)
   print "done"
   test_results2 = map(lambda p: test_classifier(train_data_scale,train_classes,test_data_scale,test_classes,p[0],p[1]),
                       classifiers) 
   out2 = open(sys.argv[5],'w')
   out2.write("\n".join(test_results2))
   out2.close()
