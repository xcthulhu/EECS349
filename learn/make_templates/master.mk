ENV=. $(BASEDIR)/venv/bin/activate && env LD_LIBRARY_PATH=$(BASEDIR)/venv/lib:$(BASEDIR)/venv/lib64/:${LD_LIBRARY_PATH}
PYTHON=$(ENV) python
MEANS=500
PERCENTAGE=0.02
