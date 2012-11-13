.PRECIOUS: folds-hogs-Stanford40 folds/reference/Stanford40
BASEDIR=..
ENV=. $(BASEDIR)/venv/bin/activate && env LD_LIBRARY_PATH=$(BASEDIR)/venv/lib:$(BASEDIR)/venv/lib64/:${LD_LIBRARY_PATH}
PYTHON=$(ENV) python
all : Stanford40-hogs-means

# Get K-Folds
FOLDS=40
folds/reference/% : ../reference/%
	$(PYTHON) ./k-fold_cross.py $(FOLDS) '$</*.jpg' $@

folds/reference/%.txt : folds/%

folds/hogs/% : folds/reference/%
	@ mkdir -p $(dir $@)
	sed -e 's/..\/reference/hogs/' -e 's/.jpg$$/-hog.npy/' $< > $@

folds-hogs-% : folds/reference/%
	@ for f in $</*.txt ; do make $(shell echo $@ | sed -e 's/-/\//g')/`basename $$f` ; done
	touch $@

# Extract Histogram of Oriented Gradients
hogs/%-hog.npy : ../reference/%.jpg
	@ mkdir -p $(dir $@)
	$(PYTHON) hog.py $< $@

hogs-% : ../reference/%
	@ mkdir -p hogs/$(@:-hogs=)
	@ for i in $</*.jpg; do make `echo $$i | sed -e 's/..\/reference/hogs/' -e 's/.jpg/-hog.npy/'` ; done
	touch $@

# Distribute work on QUEST
scripts/%_qsub.sh :
	@ mkdir -p $(dir $@)
	cat qsub.tmpl > $@
	echo "make -C $(CURDIR) $(patsubst scripts/%-qsub.sh,%,$@)" >> $@
	chmod +x $@

%_qsub : 
	@ mkdir -p out ; mkdir -p error
	make scripts/$@.sh
	qsub -o out/$@ -e error/$@ -N $@ scripts/$@

# Get K-Means
MEANS=500
PERCENTAGE=0.02
means-% : folds-%
	@ for f in $(shell echo $< | sed -e 's/-/\//g')/*-train.txt ; do make `echo $$f | sed -e 's/folds\/\(.*\)-train.txt$$/means\/\1-means-$(MEANS)-$(PERCENTAGE).npy/'` ; done
	touch $@

qsub-means-% : folds-%
	@ for f in $(shell echo $< | sed -e 's/-/\//g')/*-train.txt ; do make `echo $$f | sed -e 's/folds\/\(.*\)-train.txt$$/\1_qsub_means/' -e 's/\//-/g'` ; done

scripts/%_qsub_means.sh :
	@ mkdir -p $(dir $@)
	cat qsub.tmpl > $@
	echo "make -C $(CURDIR) $(patsubst scripts/%_qsub_means.sh,means/%-means-$(MEANS)-$(PERCENTAGE).npy, \
                                  $(shell echo $@ | sed -e 's/-/\//'))" >> $@
	chmod +x $@

%_qsub_means : 
	@ mkdir -p out ; mkdir -p error
	make scripts/$(shell echo $(@:=.sh) | sed -e 's/-/\//')
	qsub -o out/$@ -e error/$@ -N $@ scripts/$(shell echo $(@:=.sh) | sed -e 's/-/\//')

means/hogs/%-means-$(MEANS)-$(PERCENTAGE).npy : folds/hogs/%-train.txt
	@ mkdir -p $(dir $@)
	$(PYTHON) sample_k_means.py $(MEANS) $(PERCENTAGE) 243 $@ $<

# Get Bags Of Words
bows-train-% : 
	@ for i in folds/$(shell echo $@ | cut -d'-' -f3- | sed -e 's/-/\//g')/*-train.txt ; do make $(shell echo $@ | sed -e 's/-/\//g')/`basename $$i | sed -e 's/-train.txt$$//'`-bows ; done
	touch $@

bows-test-% : 
	@ for i in folds/$(shell echo $@ | cut -d'-' -f3- | sed -e 's/-/\//g')/*-test.txt ; do make $(shell echo $@ | sed -e 's/-/\//g')/`basename $$i | sed -e 's/-test.txt$$//'`-bows ; done
	touch $@
	
bows/train/%-bows : means/%-means-$(MEANS)-$(PERCENTAGE).npy folds/%-train.txt
	@ mkdir -p $(dir $@)
	$(PYTHON) bow.py $^ $(dir $@)

clean :
	rm -rf *.png *.pgm *.npy *.db *.pyc hogs datasets folds *-means
