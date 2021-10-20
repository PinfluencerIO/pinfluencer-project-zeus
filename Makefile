build-PinfluencerFunction:
	cp functions/requirements.txt $(ARTIFACTS_DIR)
	python -m pip install -r functions/requirements.txt -t $(ARTIFACTS_DIR)
	cp -r ${PWD}/*.py $(ARTIFACTS_DIR)
	mkdir $(ARTIFACTS_DIR)/functions
	cp -r functions/. $(ARTIFACTS_DIR)/functions
	echo ${PWD}
	find $(ARTIFACTS_DIR)/. -type d -name '.pytest_cache' -exec rm -rf {} \;