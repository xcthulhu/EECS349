all : venv pip-packages

venv :
	virtualenv venv

pip-packages :
	. venv/bin/activate && pip install -r requirements.txt
	touch $@

clean : 
	rm -rf venv pip-packages
