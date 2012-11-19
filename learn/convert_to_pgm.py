#!/usr/bin/env python
import Image
import sys

if __name__ == "__main__":
   im = Image.open(sys.argv[1])
   im.convert('L').save('/dev/stdout','PPM')
