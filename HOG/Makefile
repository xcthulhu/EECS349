.PRECIOUS: folds/% %-hogs %.txt %.hogs %-hog.npy %-hog-folds
BASEDIR=..
ENV=. $(BASEDIR)/venv/bin/activate && env LD_LIBRARY_PATH=$(BASEDIR)/venv/lib:$(BASEDIR)/venv/lib64/:${LD_LIBRARY_PATH}
PYTHON=$(ENV) python
all : Stanford40-hogs-means

# Get K-Folds
FOLDS=40
folds/% : ../reference/%
	$(PYTHON) ./k-fold_cross.py $(FOLDS) '$</*.jpg' $@

folds/%.txt : folds/%

folds/%.hogs : folds/%.txt
	sed -e 's/..\/reference/hogs/' -e 's/.jpg$$/-hog.npy/' $< > $@

%-hog-folds : folds/%
	@ for f in $</*.txt ; do make `echo $$f | sed -e 's/.txt$$/.hogs/'` ; done
	touch $@

# Extract Histogram of Oriented Gradients
hogs/%-hog.npy : ../reference/%.jpg
	@ mkdir -p $(dir $@)
	$(PYTHON) hog.py $< $@

%-hogs : ../reference/%
	@ mkdir -p hogs/$(@:-hogs=)
	@ for i in $</*.jpg; do make `echo $$i | sed -e 's/..\/reference/hogs/' -e 's/.jpg/-hog.npy/'` ; done
	touch $@

# Distribute work on QUEST
scripts/%-qsub.sh :
	@ mkdir -p $(dir $@)
	cat qsub.tmpl > $@
	echo "make -C $(CURDIR) $(patsubst scripts/%-qsub.sh,%,$@)" >> $@
	chmod +x $@

qsub-% : 
	@ mkdir -p out ; mkdir -p error
	make scripts/$(patsubst qsub-%,%-qsub.sh,$@)
	qsub -o out/$(patsubst qsub-%,%,$@) -e error/$(patsubst qsub-%,%,$@) -N $(patsubst qsub-%,%,$@) scripts/$(patsubst qsub-%,%-qsub.sh,$@)

# Get K-Means
MEANS=500
PERCENTAGE=0.02
%-hog-means : %-hog-folds
	@ for f in folds/$(@:-hog-means=)/*-train.hogs ; do make `echo $$f | sed -e 's/folds\/\(.*\)-train.hogs$$/means\/hog\/\1-means-$(MEANS)-$(PERCENTAGE).npy/'` ; done
	touch $@

%-qsub-hog-means : %-hog-folds
	@ for f in folds/$(@:-qsub-hog-means=)/*-train.hogs ; do make `echo $$f | sed -e 's/folds\///' -e 's/\//_/' -e 's/-train.hogs$$/-qsub-hog-means-job/'`; done
	touch $@

scripts/%-qsub-hog-means.sh :
	@ mkdir -p $(dir $@)
	cat qsub.tmpl > $@
	echo "make -C $(CURDIR) $(patsubst scripts/%-qsub-hog-means.sh,means/hog/%-means-$(MEANS)-$(PERCENTAGE).npy,$@)" | sed -e 's/_/\//g' >> $@
	chmod +x $@

%-qsub-hog-means-job : 
	@ mkdir -p out ; mkdir -p error
	make scripts/$(@:-job=.sh)
	qsub -o out/$(@:-qsub-hog-means=-hog-means) -e error/$(@:-qsub-hog-means=-hog-means) -N $@ scripts/$(@:-job=.sh)

means/hog/%-means-$(MEANS)-$(PERCENTAGE).npy : folds/%-train.hogs
	@ mkdir -p $(dir $@)
	$(PYTHON) sample_k_means.py $(MEANS) $(PERCENTAGE) 243 $@ $<

# Get Bags Of Words
%-bows : %-means
	@ mkdir -p bows/$(@:-bows=)
	@ for i in hogs/$(@:-bows=)/*-hog.npy; do make `echo $$i | sed -e 's/hogs/bows/' -e 's/-hog.npy/-bow.npy/'` ; done
	touch $@
	
bows/%-bow.npy : hogs/%-hog.npy
	@ mkdir -p $(dir $@)
	$(PYTHON) bow.py $(MEANS)-$(PERCENTAGE)-$(patsubst bows/%/,%,$(dir $@))-means.npy $< $@

clean :
	rm -rf *.png *.pgm *.npy *.db *.pyc hogs datasets folds *-means
