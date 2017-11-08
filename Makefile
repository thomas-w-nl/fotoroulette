.PHONY: install shell run 

run:
	source env/bin/activate;
	python src/main.py;

shell:
	source env/bin/activate; \
	bpython;


install:
	python3 -m venv --prompt "pi" --system-site-packages env
	source env/bin/activate; \
	pip install -r Requirements.txt;
