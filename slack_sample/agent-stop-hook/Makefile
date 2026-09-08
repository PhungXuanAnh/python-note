.DEFAULT_GOAL := help
PYTHON ?= python3
INSTALL_ARGS ?=

.PHONY: help install install-global install-claude-code install-codex install-copilot install-kiro dry-run test

help:
	@printf '%s\n' \
	  'make install             Install all four global Slack Stop hooks' \
	  'make install-claude-code Install only Claude Code (also: codex, copilot, kiro)' \
	  'make dry-run             Preview destinations and hook commands' \
	  'make test                Run offline hook and installer tests' \
	  'INSTALL_ARGS="..."       Extra install_hooks.py options (see --help)'

install install-global:
	@$(PYTHON) install_hooks.py $(INSTALL_ARGS)

install-claude-code install-codex install-copilot install-kiro:
	@$(PYTHON) install_hooks.py $(@:install-%=%) $(INSTALL_ARGS)

dry-run:
	@$(PYTHON) install_hooks.py --dry-run $(INSTALL_ARGS)

test:
	@$(PYTHON) -m unittest discover -s . -p 'test_*.py'
