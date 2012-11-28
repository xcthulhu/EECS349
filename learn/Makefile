.SECONDARY :
BASEDIR=..
include make_templates/master.mk

all : folds/Stanford40 folds/eecs_data

# Distribute work on QUEST
scripts/qsub-%.sh :
	@ mkdir -p $(dir $@)
	cat qsub.tmpl > $@
	echo "make -C $(CURDIR) $(patsubst scripts/qsub-%.sh,%,$@)" >> $@
	chmod +x $@

qsub-% : 
	@ mkdir -p out ; mkdir -p error
	make scripts/$@.sh
	qsub -o out/$@ -e error/$@ -N $@ scripts/$@.sh

# Get K-Folds
FOLDS=40
folds/% : %.tsv
	$(PYTHON) ./k-fold_cross.py $(FOLDS) $< $@
	@ for d in $@/* ; do \
		echo "echo BASEDIR=$(BASEDIR)/../../.. > $$d/Makefile" ; \
		echo BASEDIR=$(BASEDIR)/../../.. > $$d/Makefile ; \
		echo "echo REFERENCE=$(notdir $@) >> $$d/Makefile" ; \
		echo REFERENCE=$(notdir $@) >> $$d/Makefile ; \
		echo "echo include \"\$$(BASEDIR)/learn/make_templates/fold.mk\" >> $$d/Makefile" ; \
		echo include "\$$(BASEDIR)/learn/make_templates/fold.mk" >> $$d/Makefile ; \
	done

folds_% :
	make $(shell echo $@ | cut -d'_' -f1,2 | sed -e 's/_/\//g')
	make -C $(shell echo $@ | sed -e 's/_/\//g')

folds-%-qsub : folds/%
	@ for d in $</* ; do \
		echo make qsub-`echo $$d | sed -e 's/\//_/g'` ; \
		make qsub-`echo $$d | sed -e 's/\//_/g'` ; \
	done

# Extract Histogram of Oriented Gradients
hogs/%.npy : %
	@ mkdir -p $(dir $@)
	$(PYTHON) hog.py $< $@

sifts/%.npy : %
	@ mkdir -p $(dir $@)
	$(PYTHON) convert_to_pgm.py $< | siftfast | ./sift.py $@

hogs-% sifts-% : %.tsv %
	@ mkdir -p $(shell echo $@ | sed -e 's/-/\//g')
	@ cut -f1 $< | ./randomize_lines.py | while read i; do mkdir -p $(shell echo $@ | cut -d'-' -f1)/`dirname $$i` ; make $(shell echo $@ | cut -d'-' -f1)/$$i.npy ; done
	touch $@

clean :
	rm -rf *.png *.pgm *.npy *.db *.pyc hogs datasets folds *-means
