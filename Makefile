.PRECIOUS: *.npy *.db
ENV=. venv/bin/activate &&
PYTHON=$(ENV) python

all : deviantart-photos-db 500-means.npy 1000-means.npy

# Virtual Environment stuff
virtualenv.py :
	wget --no-check-certificate https://raw.github.com/pypa/virtualenv/master/virtualenv.py -O $@

venv : virtualenv.py
	rm -rf $@
	python virtualenv.py -p python2.7 $@    

requirements : freeze.txt venv
	$(ENV) pip install -r $<
	touch $@

freeze.txt :
	$(ENV) pip freeze > $@

clean :
	rm -rf *.png *.pgm *.npy *.db *.pyc hogs datasets
