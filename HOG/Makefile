.PRECIOUS: *.npy *.db
ENV=. ../venv/bin/activate &&
PYTHON=$(ENV) python
all : Stanford40-hogs

# Extract Histogram of Origiented Gradients
hogs/%-hog.npy : ../reference/%.jpg
	@ mkdir -p $(dir $@)
	$(PYTHON) hog.py $< $@

%.sh :
	cat qsub.tmpl > $@
	echo "make -C $(CURDIR) $(@:.sh=)" >> $@
	chmod +x $@

qsub-% : %.sh
	@ mkdir -p out ; mkdir -p error
	qsub -o out/$(<:.sh=) -e error/$(<:.sh=) -N $(<:.sh=) $<

%-hogs : ../reference/%
	@ mkdir -p hogs/$(@:-hogs=)
	@ for i in $</*.jpg; do make `echo $$i | sed -e 's/..\/reference/hogs/' -e 's/.jpg/-hog.npy/'` ; done
	touch $@

MEANS=100000
PERCENTAGE=0.2
%-means.npy : %-hogs
	$(PYTHON) sample_k_means.py $(MEANS) $(PERCENTAGE) 243 $@ 'hogs/$(<:-hogs=/*-hog.npy)'

clean :
	rm -rf *.png *.pgm *.npy *.db *.pyc hogs datasets
