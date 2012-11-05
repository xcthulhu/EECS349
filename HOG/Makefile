.PRECIOUS: *.npy *.db
ENV=. ../venv/bin/activate &&
PYTHON=$(ENV) python

all : deviantart-photos-db 500-means.npy 1000-means.npy

# Extract Histogram of Origiented Gradients
hogs/%-hog.npy : ../reference/%.jpg
	@ mkdir -p $(dir $@)
	$(PYTHON) hog.py $< $@

%-hogs : ../reference/%
	@ mkdir -p hogs/$(@:-HOGS=)
	@ for i in $</*.jpg; do make `echo $$i | sed -e 's/..\/reference/hogs/' -e 's/.jpg/-hog.npy/'` ; done
	toch $@

%-means.npy : %-HOGS
	$(PYTHON) sample_k_means.py $(@:-means.npy=) 0.05 243 $@ hogs/$(<:-HOGS=/*.npy)

clean :
	rm -rf *.png *.pgm *.npy *.db *.pyc hogs datasets
