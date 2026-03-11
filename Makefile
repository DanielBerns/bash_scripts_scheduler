# Makefile for YAML Cron Scheduler

# Variables
DEST_DIR = ~/Commands
SCRIPT = ./scripts/scheduler.py
CONFIG = schedule.yaml
LOG_FILE = schedule.log
ASSETS_DIR = ./assets

.PHONY: help sync clear status logs init

# Default target when just typing 'make'
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  init      Create $(DEST_DIR), copy dummy_script.sh and schedule.yaml from ASSETS_DIR"
	@echo "  sync      Apply the jobs defined in $(CONFIG) to crontab"
	@echo "  clear     Remove all managed jobs from crontab"
	@echo "  status    List all currently managed jobs in crontab"
	@echo "  logs      Tail the execution log file ($(LOG_FILE))"

init:
	@echo "Creating $(DEST_DIR) if it does not exist..."
	mkdir -p $(DEST_DIR)
	@echo "Copying assets from $(ASSETS_DIR)..."
	cp $(ASSETS_DIR)/dummy_task.sh $(DEST_DIR)/
	cp $(ASSETS_DIR)/schedule.yaml $(DEST_DIR)/
	@echo "Setting execution permissions for the dummy script..."
	chmod +x $(DEST_DIR)/dummy_task.sh
	@echo "Initialization complete. You can now run 'make sync' from $(DEST_DIR)."

sync:
	uv run $(SCRIPT) sync

clear:
	uv run $(SCRIPT) clear

status:
	uv run $(SCRIPT) status

logs:
	tail -f $(LOG_FILE)
