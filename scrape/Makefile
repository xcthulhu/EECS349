ENV=. ../venv/bin/activate &&
PYTHON=$(ENV) python

all : dog-tag-photos puppy-tag-photos kittens-tag-photos cat-tag-photos earthporn-tag-photos nicolas+cage-tag-photos 

../venv :
	make -C $(dir $@) requirements

%-tag-photos :
	$(PYTHON) tumblrscraper.py tag $(@:-tag-photos=) 100000
	touch $@

%-blog-photos :
	$(PYTHON) tumblrscraper.py blog $(@:-blog-photos=) 100000
	touch $@

clean :
	rm -f *.db *.pyc
