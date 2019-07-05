SHELL := /bin/bash

USER=sigma
HOST=192.168.1.200

DESTINATION_SERVER=$(USER)@$(HOST)
RSYNC_PARAMS='-avlP --exclude .venv'

DESTINATION_PATH=/home/$(USER)/spark/pyspark-sample

all:
	eval rsync $(RSYNC_PARAMS) . $(DESTINATION_SERVER):$(DESTINATION_PATH)
	