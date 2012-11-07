#!/usr/bin/env python

import tumblpy
import sqlite3
import ts_model
import sys

def tumblr_scraper(base_url,db_name,num_images,start_offset=0,limit=20,url_type='blog',tag=None):
    #init with some key
    t = tumblpy.Tumblpy(app_key = 'V55FKUe1lMSdx0UyGSFknmO8DoSaeNzT9oByUwOE1Hvp7diQJ7',
                        app_secret = 'TD9eTgRhoo8ceu0cjcF0nROWAAMkst1uAkSx5XuSOjnYxrGq50',
                        callback_url = 'whatever.com/notimportant_now')

    #we don't need this code
    auth_props = t.get_authentication_tokens()
    auth_url = auth_props['auth_url']
    oauth_token = auth_props['oauth_token']
    oauth_token_secret = auth_props['oauth_token_secret']

    #running
    #get db connection
    print "Connecting to %s" % db_name
    conn = ts_model.touch_db(db_name)
    c = conn.cursor()
    #scraping...
    if url_type == 'blog': print "Scraping %s" % base_url
    else : print "Scraping %s" % tag
    n = ts_model.photo_count(conn)
    if url_type == 'tag' : i = ts_model.min_time(conn)
    else : i = 0
    while n < num_images :
        #get the posts
        if url_type == 'blog':
            print "Get posts %i to %i" % (i*limit+start_offset,(1+i)*limit+start_offset)
            posts = t.get('posts',blog_url=base_url,extra_endpoints='photo', params={'limit':limit, 'offset':i*limit+start_offset})
            posts = posts['posts']
        if url_type == 'tag':
            print "Get posts %i posts before timestamp %i" % (limit,i)
            params = {'limit':limit, 'tag':tag, 'before':i};
            posts = t.get(None,blog_url=None,tag=True, params=params)
        oldi = i
        for p in posts:
          #some posts don't have photo
          if(not('photos' in  p)): continue
          #some posts have more than one image, we will ignore that for now
          if(len(p['photos']) != 1): continue
          #some posts don't have tag
          if(len(p['tags']) == 0): continue
          # If we made it through that, we have a new photo
          n += 1
          # we need timestamp
          i = p['timestamp']
          #print out the info, move to DB later
          tags = [ y.strip().lower() for x in p['tags']
                                     for y in x.split('\n') ]
          url = p['photos'][0]['original_size']['url']
          # if this is slow, switch to batch execute instead
          if 'note_count' in p.keys():
              note_count = p['note_count']
          else:
              note_count = -1
          if tag : print "At %i found %s %i (notes=%i): %s %s" % (i, tag, n, note_count, url,
                                                                  "#" + " #".join(tags))
          ts_model.add_tags(c, tags)
          ts_model.add_photo(c, url, note_count, i)
          ts_model.link_tags_photo(c, tags, url)
          conn.commit()
        # Decrement the timestamp if it didn't change
        if oldi == i: i -= limit
    conn.close()

if __name__ == "__main__" :
    base_url=None
    tag=None
    if sys.argv[1] == 'blog':
        base_url='http://%s.tumblr.com' % sys.argv[2]
    else:
        tag = sys.argv[2]
    db_name = '%s.db' % sys.argv[2]
    num_images = int(sys.argv[3])
    if len(sys.argv) >= 5:
       start_offset = int(sys.argv[4])
    else :
       start_offset = 0
    if tag:
        tumblr_scraper(None, db_name, num_images, start_offset=start_offset, limit=20, url_type='tag',tag=tag)
    else:
        tumblr_scraper(base_url,db_name,num_images,start_offset=start_offset,limit=20)
