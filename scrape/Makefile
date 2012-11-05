ENV=. ../venv/bin/activate &&
PYTHON=$(ENV) python

all : deviantart-photos

../venv :
	make -C $(dir $@) requirements

%-photos :
	$(PYTHON) tumblrscraper.py $(@:-photos=) 10000
	touch $@

clean :
	rm -f *.db *.pyc
