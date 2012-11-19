.PRECIOUS: *.npy *.db
ENV=. venv/bin/activate &&
PYTHON=$(ENV) python

all : 500-means.npy 1000-means.npy

# Virtual Environment stuff
virtualenv.py :
	wget --no-check-certificate https://raw.github.com/pypa/virtualenv/master/virtualenv.py -O $@

venv : virtualenv.py
	rm -rf $@
	python2.7 virtualenv.py --system-site-packages -p python2.7 $@    

flann : venv
	@ mkdir -p venv/src
	cd venv/src && wget http://people.cs.ubc.ca/~mariusm/uploads/FLANN/flann-1.7.1-src.zip
	cd venv/src && unzip flann-1.7.1-src.zip
	mkdir -p venv/src/flann-1.7.1-src/build
	cd venv/src/flann-1.7.1-src/build && cmake -DCMAKE_INSTALL_PREFIX:PATH=$(CURDIR)/venv ..
	make -C venv/src/flann-1.7.1-src/build install
	touch $@

libsiftfast : venv
	@ mkdir -p venv/src
	cd venv/src && wget http://downloads.sourceforge.net/project/libsift/libsiftfast/libsiftfast-1.2/libsiftfast-1.2-src.tgz
	cd venv/src && tar zxfv libsiftfast-1.2-src.tgz
	make -C venv/src/libsiftfast-1.2-src prefix=$(CURDIR)/venv 
	make -C venv/src/libsiftfast-1.2-src install
	touch $@

requirements : freeze.txt flann venv
	$(ENV) pip install -r $<
	touch $@

freeze.txt :
	$(ENV) pip freeze > $@

clean :
	rm -rf *.png *.pgm *.npy *.db *.pyc hogs datasets
