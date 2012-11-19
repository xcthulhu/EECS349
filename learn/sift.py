#!/usr/bin/env python
import sys
import numpy as np
import fileinput

if __name__ == "__main__":
   sifts = \
       [ np.array(
         map(float,
         # Each line needs to be stripped, and cleaned up a bit
         line.strip().replace(' \n',' ').replace('\n',' ').split(' ')))
         for line in sys.stdin.read().split('\n\n')
         if line != '' ]
   sifts[0] = sifts[0][2:]
   np.save(sys.argv[1],np.vstack(sifts))
