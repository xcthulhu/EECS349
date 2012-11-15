.PRECIOUS : 
include $(BASEDIR)/learn/make_templates/master.mk
all : hog-features
hog-features : hogs-test hogs-train hogs/means.npy hogs/means.flann bag_of_words-flann-hogs bag_of_words-true-hogs 

hogs-% : %.txt
	@ while read line; do \
		echo make hogs/$(<:.txt=)/`basename $$line | sed -e 's/.jpg$$/.npy/'` ; \
		make hogs/$(<:.txt=)/`basename $$line | sed -e 's/.jpg$$/.npy/'` ; \
	done < $<
	touch $@

$(BASEDIR)/learn/hogs/$(REFERENCE)/%.npy :
	make -C $(BASEDIR)/learn hogs/$(REFERENCE)/$(notdir $@)
	
hogs/train/%.npy hogs/test/%.npy : $(BASEDIR)/learn/hogs/$(REFERENCE)/%.npy
	@ mkdir -p $(dir $@)
	ln -s $(shell python -c 'import os ; print os.path.abspath("$<")') $@

%/means.npy : %-train
	@ mkdir -p $(dir $@)
	$(PYTHON) $(BASEDIR)/learn/sample_k_means.py $(MEANS) $(PERCENTAGE) 243 $@ '$(<:-train=)/train/*.npy'

%/means.flann : %/means.npy
	$(PYTHON) $(BASEDIR)/learn/mk_flann.py $(FLANN_PRECISION) $< $@ $@.params

%/means.flann.params : %/means.flann

bag_of_words-% : bows-%-train bows-%-test
	echo $@

bows-flann-%-train : %/means.npy %/means.flann %/means.flann.params %-train
	@ mkdir -p $(shell echo $@ | sed -e 's/-/\//g')
	$(PYTHON) $(BASEDIR)/learn/bow_flann.py $< $(<:.npy=.flann) $(<:.npy=.flann.params) '$(patsubst bows-flann-%-train,%/train,$@)/*.npy' $(shell echo $@ | sed -e 's/-/\//g')
	touch $@

bows-flann-%-test : %/means.npy %/means.flann %/means.flann.params %-test
	@ mkdir -p $(shell echo $@ | sed -e 's/-/\//g')
	$(PYTHON) $(BASEDIR)/learn/bow_flann.py $< $(<:.npy=.flann) $(<:.npy=.flann.params) '$(patsubst bows-flann-%-test,%/test,$@)/*.npy' $(shell echo $@ | sed -e 's/-/\//g')
	touch $@

bows-true-%-train : %/means.npy %-train
	@ mkdir -p $(shell echo $@ | sed -e 's/-/\//g')
	$(PYTHON) $(BASEDIR)/learn/bow_slow.py $< '$(patsubst bows-true-%-train,%/train,$@)/*.npy' $(shell echo $@ | sed -e 's/-/\//g')
	touch $@

bows-true-%-test : %/means.npy %-test
	@ mkdir -p $(shell echo $@ | sed -e 's/-/\//g')
	$(PYTHON) $(BASEDIR)/learn/bow_slow.py $< '$(patsubst bows-true-%-test,%/test,$@)/*.npy' $(shell echo $@ | sed -e 's/-/\//g')
	touch $@

clean :
	rm -rf hogs *-*
