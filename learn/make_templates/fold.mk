.SECONDARY:
include $(BASEDIR)/learn/make_templates/master.mk
all : hog-features
hog-features : hogs/test.txt hogs/train.txt hogs/means.npy hogs/means.flann bag_of_words-flann-hogs bag_of_words-true-hogs class-flann-hogs-scaled.txt class-true-hogs-scaled.txt
sift-features : sifts/test.txt sifts/train.txt sifts/means.npy sifts/means.flann bag_of_words-flann-sifts bag_of_words-true-sifts

hogs/%.txt sifts/%.txt : %.txt
	@ mkdir -p $(dir $@)
	rm -f $@
	@ while read line; do \
		echo make $(BASEDIR)/learn/$(dir $@)/$(REFERENCE)/`basename $$line | sed -e 's/.jpg$$/.npy/'` ; \
		make $(BASEDIR)/learn/$(dir $@)/$(REFERENCE)/`basename $$line | sed -e 's/.jpg$$/.npy/'` ; \
		echo "echo $(BASEDIR)/learn/$(dir $@)/$(REFERENCE)/`basename $$line | sed -e 's/.jpg$$/.npy/'` >> $@" ; \
		echo $(BASEDIR)/learn/$(dir $@)/$(REFERENCE)/`basename $$line | sed -e 's/.jpg$$/.npy/'` >> $@ ; \
	done < $<

$(BASEDIR)/learn/hogs/$(REFERENCE)/%.npy :
	make -C $(BASEDIR)/learn hogs/$(REFERENCE)/$(notdir $@)

$(BASEDIR)/learn/sifts/$(REFERENCE)/%.npy :
	make -C $(BASEDIR)/learn sifts/$(REFERENCE)/$(notdir $@)

hogs/means.npy : %/train.txt
	@ mkdir -p $(dir $@)
	$(PYTHON) $(BASEDIR)/learn/sample_k_means.py $(MEANS) $(HOG_PERCENTAGE) $(HOG_DIMENSIONS) $@ $<

sifts/means.npy : %/train.txt
	@ mkdir -p $(dir $@)
	$(PYTHON) $(BASEDIR)/learn/sample_k_means.py $(MEANS) $(SIFT_PERCENTAGE) $(SIFT_DIMENSIONS) $@ $<

%/means.flann : %/means.npy
	$(PYTHON) $(BASEDIR)/learn/mk_flann.py $(FLANN_PRECISION) $< $@ $@.params

%/means.flann.params : %/means.flann

bag_of_words-% : bows-%-train bows-%-test
	touch $@

bows-flann-%-train : %/means.npy %/means.flann %/means.flann.params
	@ mkdir -p $(shell echo $@ | sed -e 's/-/\//g')
	$(PYTHON) $(BASEDIR)/learn/bow_flann.py $< $(<:.npy=.flann) $(<:.npy=.flann.params) '$(patsubst bows-flann-%-train,%/train,$@).txt' $(shell echo $@ | sed -e 's/-/\//g')
	touch $@

bows-flann-%-test : %/means.npy %/means.flann %/means.flann.params
	@ mkdir -p $(shell echo $@ | sed -e 's/-/\//g')
	$(PYTHON) $(BASEDIR)/learn/bow_flann.py $< $(<:.npy=.flann) $(<:.npy=.flann.params) '$(patsubst bows-flann-%-test,%/test,$@).txt' $(shell echo $@ | sed -e 's/-/\//g')
	touch $@

bows-true-%-train : %/means.npy
	@ mkdir -p $(shell echo $@ | sed -e 's/-/\//g')
	$(PYTHON) $(BASEDIR)/learn/bow_slow.py $< '$(patsubst bows-true-%-train,%/train,$@).txt' $(shell echo $@ | sed -e 's/-/\//g')
	touch $@

bows-true-%-test : %/means.npy
	@ mkdir -p $(shell echo $@ | sed -e 's/-/\//g')
	$(PYTHON) $(BASEDIR)/learn/bow_slow.py $< '$(patsubst bows-true-%-test,%/test,$@).txt' $(shell echo $@ | sed -e 's/-/\//g')
	touch $@

class-%-unscaled.txt class-%-scaled.txt : bag_of_words-%
	$(PYTHON) $(BASEDIR)/learn/classify.py 'bows/$(shell echo $(patsubst bag_of_words-%,%,$<) | sed -e 's/-/\//')/train/*.npy' 'bows/$(shell echo $(patsubst bag_of_words-%,%,$<) | sed -e 's/-/\//')/test/*.npy' $(MEANS) $(patsubst bag_of_words-%,class-%-scaled.txt,$<) $(patsubst bag_of_words-%,class-%-unscaled.txt,$<)

clean :
	rm -rf hogs *-*
