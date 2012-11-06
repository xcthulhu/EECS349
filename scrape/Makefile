ENV=. ../venv/bin/activate &&
PYTHON=$(ENV) python

all : deviantart-photos

../venv :
	make -C $(dir $@) requirements

%-tag-photos :
	$(PYTHON) tumblrscraper.py tag $(@:-tag-photos=) 1000000
	touch $@

%-blog-photos :
	$(PYTHON) tumblrscraper.py tag $(@:-blog-photos=) 1000000
	touch $@

clean :
	rm -f *.db *.pyc
