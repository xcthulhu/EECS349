include $(BASEDIR)/learn/make_templates/master.mk
all : hog-features
hog-features : hogs-test hogs-train hogs/means.npy hogs/means.flann bag_of_words-hogs

hogs-% : %.txt
	@ while read line; do \
		echo make hogs/$(<:.txt=)/`basename $$line | sed -e 's/.jpg$$/-hog.npy/'` ; \
		make hogs/$(<:.txt=)/`basename $$line | sed -e 's/.jpg$$/-hog.npy/'` ; \
	done < $<
	touch $@

$(BASEDIR)/learn/hogs/$(REFERENCE)/%-hog.npy :
	make -C $(BASEDIR)/learn hogs/$(REFERENCE)/$(notdir $@)
	
hogs/train/%.npy hogs/test/%.npy : $(BASEDIR)/learn/hogs/$(REFERENCE)/%.npy
	@ mkdir -p $(dir $@)
	ln -s $(shell python -c 'import os ; print os.path.abspath("$<")') $@

%/means.npy : %-train
	@ mkdir -p $(dir $@)
	$(PYTHON) $(BASEDIR)/learn/sample_k_means.py $(MEANS) $(PERCENTAGE) 243 $@ '$(<:-train=)/train/*.npy'

%/means.flann : %/means.npy
	$(PYTHON) $(BASEDIR)/learn/mk_flann.py $< $@

bag_of_words-% : bows-%-train bows-%-test
	touch $@

bows-%-train : %/means.npy %/means.flann # %-train
	@ mkdir -p $(shell echo $@ | sed -e 's/-/\//g')
	$(PYTHON) $(BASEDIR)/learn/bow.py $< '$(patsubst bows-%-train,%/train,$@)/*.npy' $(shell echo $@ | sed -e 's/-/\//g')
	touch $@

bows-%-test : %/means.npy %-test
	@ mkdir -p $(shell echo $@ | sed -e 's/-/\//g')
	$(PYTHON) $(BASEDIR)/learn/bow.py $< '$(patsubst bows-%-test,%/test,$@)/*.npy' $(shell echo $@ | sed -e 's/-/\//g')
	touch $@

clean :
	rm -rf hogs *-*
