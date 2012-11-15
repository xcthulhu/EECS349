#!/usr/bin/env python
import sqlite3
import ts_model
from urllib import urlretrieve
import os
import sys

def download(db_name, directory, start_id=0):
    #get db connection
    print "Connecting to %s" % db_name
    print start_id
    conn = ts_model.touch_db(db_name)
    c = conn.cursor()
    if not os.path.exists(directory):
        os.makedirs(directory)
    for photo in  ts_model.get_photos(c, start_id):
	#no gif
	if photo[3].split('.')[-1] == 'gif':
		continue
        filename = photo[3].split('/')[-1]
        outpath = os.path.join(directory, filename)
	#never downloaded
	if not os.path.exists(outpath) : 
        	print 'Downloading %s' % photo[3]
        	urlretrieve(photo[3], outpath)
        	print 'Save as %s' % filename

if __name__ == "__main__":
    db_name = sys.argv[1] + '.db'
    directory = sys.argv[1]
    start_id = 0
    if len(sys.argv) > 2:
        directory = sys.argv[2]
    if len(sys.argv) > 3:
        start_id = sys.argv[3]
    download(db_name, directory, int(start_id))
