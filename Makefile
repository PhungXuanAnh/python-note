install-all-requirements:
	find . -name requirements.txt | xargs -I{} .venv/bin/pip install -r {}