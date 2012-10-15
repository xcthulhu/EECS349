TAG=$(notdir $(CURDIR))

all : $(TAG)

$(TAG) :
	../scrape.py http://www.tumblr.com/tagged/$@ 100
	touch $@

clean :
	rm -f $(TAG) *.jpg *.png
