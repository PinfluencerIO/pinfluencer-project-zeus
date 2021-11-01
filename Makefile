build-PinfluencerFunction:
	cp src/requirements.txt $(ARTIFACTS_DIR)
	python -m pip install -r src/requirements.txt -t $(ARTIFACTS_DIR)
	cp -r ${PWD}/*.py $(ARTIFACTS_DIR)
	mkdir $(ARTIFACTS_DIR)/src
	cp -r src/. $(ARTIFACTS_DIR)/src
	echo ${PWD}
	find $(ARTIFACTS_DIR)/. -type d -name '.pytest_cache' -exec rm -rf {} \;