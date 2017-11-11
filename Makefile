.PHONY: install shell run 

run:
	source python_install/bin/activate; \
	python3.6 main.py;

shell:
	source python_install/bin/activate; \
	bpython;


install:
	python3.6 -m venv --prompt "pi" --system-site-packages python_install
	source python_install/bin/activate; \
	pip3.6 install -r Requirements.txt;


