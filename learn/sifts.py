#!/usr/bin/env python
import sys
import numpy as np
import envoy

def sifts(fn):
   "Uses imagemagick convert and siftfast to extract sifts"
   sifts_txt = envoy.run('convert %s -type Grayscale pgm:- | siftfast' % fn)
   # Create Matrix
   return np.array(
          [ np.array(
            map(float,
                # Each line needs to be stripped, and cleaned up a bit
                line.strip().replace(' \n',' ').replace('\n',' ').split(' ')))
                for line in sifts_txt.std_out.split('\n\n')
                if line != '' ] )

if __name__ == "__main__":
   np.save(sys.argv[2],sifts(sys.argv[1]))
