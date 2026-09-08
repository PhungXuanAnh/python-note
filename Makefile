install-all-requirements:
	find . -name requirements.txt | xargs -I{} .venv/bin/pip install -r {}

# ----------------------------------------------------------------------------------
# The Claude Code session that DrissionPage_sample/auto_upload_image drives.
#
# The uploader runs it inside tmux so it can send prompts and screenshots without
# touching the display or stealing the focus. These targets are for you, not for it.
# Keep CC_SESSION in step with [providers.claude-code].session in that config.toml.
# ----------------------------------------------------------------------------------
CC_SESSION ?= cc

# Watch it / take over. Detach again with Ctrl-b d, which leaves the session running.
cc-attach:
	tmux attach -t $(CC_SESSION)

# What is running, if anything.
cc-status:
	@tmux has-session -t =$(CC_SESSION) 2>/dev/null \
		&& tmux display-message -p -t =$(CC_SESSION): \
			'session $(CC_SESSION): running [#{pane_current_command}] started as [#{pane_start_command}]' \
		|| echo "session $(CC_SESSION): not running"

# Stop it. The next run starts a fresh one with the model/effort from config.toml.
cc-kill:
	tmux kill-session -t =$(CC_SESSION)

install-stop-slack-hooks:
	@$(MAKE) -C slack_sample/agent-stop-hook install

.PHONY: install-all-requirements cc-attach cc-status cc-kill install-stop-slack-hooks
