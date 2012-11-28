#!/usr/bin/env python

import sys
from random import shuffle

if __name__ == "__main__":
	lines = sys.stdin.readlines()
	shuffle(lines)
	for l in lines:
		print l.strip()
