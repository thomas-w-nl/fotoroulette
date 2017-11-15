.PHONY: install shell run 

run:
	source python_install/bin/activate; \
	python main.py;

shell:
	source python_install/bin/activate; \
	bpython;


install:
	python -m venv --prompt "pi" --system-site-packages python_install
	source python_install/bin/activate; \
	pip install -r Requirements.txt;


