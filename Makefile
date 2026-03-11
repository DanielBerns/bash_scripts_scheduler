# Makefile for YAML Cron Scheduler

# Variables
DEST_DIR = ~/Commands
CRONTABS_BACKUPS = $(DEST_DIR)/crontab_backups
SCRIPT = ./scripts/scheduler.py
ASSETS_DIR = ./assets
CONFIG = schedule.yaml
LOG_FILE = schedule.log
DUMMY_TASK_SH = dummy_task.sh

.PHONY: help sync clear status logs init

# Default target when just typing 'make'
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  init      Create $(DEST_DIR), copy dummy_script.sh and $(CONFIG) from ASSETS_DIR"
	@echo "  backup    Manually backup the entire current crontab to $(CRONTABS_BACKUPS)
	@echo "  sync      Apply the jobs defined in $(DEST_DIR)/$(CONFIG) to crontab"
	@echo "  clear     Remove all managed jobs from crontab"
	@echo "  status    List all currently managed jobs in crontab"
	@echo "  logs      Tail the execution log file ($(DEST_DIR)/$(LOG_FILE))"

init:
	@echo "Creating $(DEST_DIR) if it does not exist..."
	mkdir -p $(DEST_DIR)
	@echo "Copying assets from $(ASSETS_DIR)..."
	cp $(ASSETS_DIR)/$(DUMMY_TASK_SH) $(DEST_DIR)/
	cp $(ASSETS_DIR)/$(CONFIG) $(DEST_DIR)/
	@echo "Setting execution permissions for the dummy script..."
	chmod +x $(DEST_DIR)/$(DUMMY_TASK_SH)
	@echo "Initialization complete. You can now run 'make sync' from $(DEST_DIR)."

backup:
	uv run $(SCRIPT) backup --dir $(CRONTABS_BACKUPS)

sync:
	uv run $(SCRIPT) sync

clear:
	uv run $(SCRIPT) clear

status:
	uv run $(SCRIPT) status

logs:
	tail -f ${DEST_DIR}/$(LOG_FILE)
