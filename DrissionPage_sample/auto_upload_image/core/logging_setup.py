"""Shared logging configuration."""
import logging
import sys

FORMAT = "%(levelname)-7s [%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] : %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format=FORMAT,
        datefmt=DATEFMT,
        stream=sys.stdout,
        force=True,
    )
    # DrissionPage is chatty at DEBUG level and drowns out our own messages.
    logging.getLogger("DrissionPage").setLevel(logging.WARNING)
