.PRECIOUS: *.npy *.db
ENV=. venv/bin/activate &&
PYTHON=$(ENV) python

all : Stanford40 Dogs Cats

# Dog Database
download/dogs.tar :
	@ mkdir -p $(dir $@)
	curl http://vision.stanford.edu/aditya86/ImageNetDogs/images.tar -o $@

# Cat Database
download/CAT_DATASET_01.zip :
	@ mkdir -p $(dir $@)
	curl http://137.189.35.203/WebUI/CatDatabase/Data/CAT_DATASET_01.zip -o $@

download/CAT_DATASET_02.zip :
	@ mkdir -p $(dir $@)
	curl http://137.189.35.203/WebUI/CatDatabase/Data/CAT_DATASET_02.zip -o $@

# Stanford 40
download/Stanford40_JPEGImages.zip :
	@ mkdir -p $(dir $@)
	curl http://vision.stanford.edu/Datasets/Stanford40_JPEGImages.zip -o $@

# Set up datasets
Stanford40 : download/Stanford40_JPEGImages.zip 
	rm -rf $@
	unzip $<
	mv JPEGImages $@
	touch $@

Dogs : download/dogs.tar
	rm -rf $@
	tar xfv $<
	mv Images $@
	touch $@

clean :
	rm -rf download Stanford40 JPEGImages
