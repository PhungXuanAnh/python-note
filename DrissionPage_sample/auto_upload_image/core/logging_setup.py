"""Shared logging configuration."""
import logging
import sys

# %(name)s rather than %(module)s: every provider now lives in `providers/<name>/
# provider.py`, so the module alone reads "provider." for all of them. ShortName below
# trims the logger name to its last two parts, giving "claude.provider" / "claude_code.
# provider" while leaving single-part names like "run" alone.
FORMAT = "%(levelname)-7s [%(asctime)s] [%(short_name)s.%(funcName)s:%(lineno)d] : %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"


class ShortName(logging.Filter):
    """Add ``short_name``: the tail of the logger name, at most two dotted parts."""

    def filter(self, record):
        record.short_name = ".".join(record.name.split(".")[-2:])
        return True


def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format=FORMAT,
        datefmt=DATEFMT,
        stream=sys.stdout,
        force=True,
    )
    for handler in logging.getLogger().handlers:
        handler.addFilter(ShortName())
    # DrissionPage is chatty at DEBUG level and drowns out our own messages.
    logging.getLogger("DrissionPage").setLevel(logging.WARNING)
