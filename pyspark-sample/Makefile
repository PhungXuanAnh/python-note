SHELL := /bin/bash

USER=vagrant
HOST=192.168.1.223

DESTINATION_SERVER=$(USER)@$(HOST)
RSYNC_PARAMS='-avlP --exclude .venv'

DESTINATION_PATH=/home/$(USER)/pyspark-sample

all:
	eval rsync $(RSYNC_PARAMS) . $(DESTINATION_SERVER):$(DESTINATION_PATH)
	