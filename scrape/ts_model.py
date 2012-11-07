#!/usr/bin/env python

from os.path import exists 
import sqlite3
from itertools import product
import time

def touch_db(filename) :
    if not exists(filename):
        #create the database
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS tags
                  (tag_id integer primary key autoincrement, 
                   tag text,
                   unique(tag))''')
        c.execute('''CREATE TABLE IF NOT EXISTS photos
                  (photo_id integer primary key autoincrement, 
                   note_count integer, 
                   time_stamp integer,
                   url text,
                   unique(url))''')
        c.execute('''CREATE TABLE IF NOT EXISTS photo_tags
                  (tag_id integer, 
                   photo_id integer,
                   unique (tag_id, photo_id),
                   foreign key(tag_id) references tags(tag_id),
                   foreign key(photo_id) references photos(photo_id))''')
        conn.commit()
        return conn
    else:
        return sqlite3.connect(filename)

def photo_count(c):
    return c.execute('''SELECT COUNT(*) FROM photos''').fetchone()[0]

def min_time(c):
   t = c.execute('''SELECT MIN(time_stamp) FROM photos''').fetchone()[0]
   if t : return t
   else : return int(time.mktime(time.gmtime()))
        
def add_tags(c, tags):
    c.executemany('''INSERT INTO tags (tag)
                     SELECT * FROM (SELECT ?)
                     WHERE NOT EXISTS (
                           SELECT * FROM tags WHERE tag = ?
                     ) LIMIT 1''', [(t,t) for t in tags])

def add_photo(c, url, note_count, time_stamp):
    c.execute('''INSERT INTO photos (url, note_count, time_stamp)
                 SELECT * FROM (SELECT ?, ?, ?)
                 WHERE NOT EXISTS (
                   SELECT * FROM photos WHERE url = ?
                 ) LIMIT 1''', (url, note_count, time_stamp, url))

def link_tags_photo(c, tags, url):
    photo_id = c.execute('''SELECT photo_id from photos 
                            where url = ? LIMIT 1''', 
                         (url,)).fetchone()[0]
    tag_ids = [ c.execute('''SELECT tag_id from tags 
                             where tag = ? LIMIT 1''', (t,)).fetchone()[0]
                for t in tags ]
    data = [(photo_id,t,photo_id,t) for t in tag_ids]
    c.executemany('''INSERT INTO photo_tags (photo_id, tag_id)
                     SELECT * FROM (SELECT ?, ?)
                     WHERE NOT EXISTS (
                       SELECT * FROM photo_tags
                         WHERE photo_id = ?
                         AND   tag_id = ?
                     ) LIMIT 1''', data)
