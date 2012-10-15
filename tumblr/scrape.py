#!/usr/bin/env python

import sys
import os
from pyquery import PyQuery as pq
from urllib2 import Request, urlopen
from time import sleep

def scrape_pic_srcs(d):
	"Scrapes pics from a tumblr DOM"
        links = d('a').filter('.high_res_link').find('img')
        for l in links : yield l.get('src')

def next_url(d):
	url_base = '/'.join(d.base_url.split('/')[0:3])
	return url_base + d('a#next_page_link').attr('href')

def wget(url,file_name=None):
	"Grabs a URL and saves it to a file"
	if file_name ==None: file_name = url.split('/')[-1]
	if os.path.isfile(file_name) : 
		print "File exists, skipping: " + file_name
		return
	req = Request(url)
	try:
		f = urlopen(req)
		print "Downloading " + url
		# Open our local file for writing
		local_file = open(file_name, "w")
		#Write to our local file
		local_file.write(f.read())
		local_file.close()
	#handle errors
	except HTTPError, e:
		print "HTTP Error:", e.code , url
	except URLError, e:
		print "URL Error:", e.reason , url

if __name__ == "__main__":
	url = sys.argv[1]
	times = int(sys.argv[2])
	for _ in range(times):
		d = pq(url=url)
		for l in scrape_pic_srcs(d): 
			sleep(1)
			wget(l)
		url = next_url(d)
