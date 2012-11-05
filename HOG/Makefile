.PRECIOUS: *.npy *.db
ENV=. ../venv/bin/activate &&
PYTHON=$(ENV) python

all : deviantart-photos-db 500-means.npy 1000-means.npy

# Extract Histogram of Origiented Gradients
hogs/Stanford40/%-hog.npy : ../reference/Stanford40/%.jpg
	@ mkdir -p $(dir $@)
	$(PYTHON) hog.py $< $@

%-HOGS : 
	@ mkdir -p hogs/$(@:-HOGS=)
	@ for i in $(wildcard $</*.jpg) ; do $(PYTHON) hog.py $$i hogs/; done

%-means.npy : %-HOGS
	$(PYTHON) sample_k_means.py $(@:-means.npy=) 0.05 243 $@ hogs/$(<:-HOGS=/*.npy)

clean :
	rm -rf *.png *.pgm *.npy *.db *.pyc hogs datasets
