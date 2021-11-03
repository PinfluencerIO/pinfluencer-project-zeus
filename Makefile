build-PinfluencerFunction:
	cp src/requirements.txt $(ARTIFACTS_DIR)
	python -m pip install -r src/requirements.txt -t $(ARTIFACTS_DIR)
	cp -r ./*.py $(ARTIFACTS_DIR)
	mkdir $(ARTIFACTS_DIR)/src
	cp -r src/. $(ARTIFACTS_DIR)/src