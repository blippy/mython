.PHONY : install

install : 
	python3 setup.py sdist
	pip install dist/mython-0.0.1.tar.gz --user --upgrade


