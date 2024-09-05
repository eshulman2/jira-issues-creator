# Define variables
APP_NAME := jira-issues-creator
RUN_SCRIPT := jira_issues_creator.py
SETUP_DIR := $(shell cd "$(dir $(lastword $(MAKEFILE_LIST)))" && pwd)
VENV_DIR := $(SETUP_DIR)/venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
LOCAL_BIN_DIR := $(HOME)/.local/bin
WRAPPER_SCRIPT := $(LOCAL_BIN_DIR)/$(APP_NAME)
REQUIREMENTS_FILE := $(SETUP_DIR)/requirements.txt
SCRIPT := $(SETUP_DIR)/$(RUN_SCRIPT)

# Default target: Install the tool
install: $(VENV_DIR) install-dependencies create-wrapper check-path

# Create virtual environment
$(VENV_DIR):
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_DIR)
	@echo "Upgrading pip and setuptools..."
	$(PIP) install --upgrade pip setuptools

# Install dependencies from a requirements file
install-dependencies:
	@echo "Installing dependencies from $(REQUIREMENTS_FILE)..."
	$(PIP) install -r $(REQUIREMENTS_FILE)

# Create a wrapper script for easy command execution
create-wrapper:
	@echo "Creating wrapper script..."
	@mkdir -p $(LOCAL_BIN_DIR)  # Use local bin directory variable
	@echo "#!/bin/sh" > $(WRAPPER_SCRIPT)
	@echo 'exec $(PYTHON) $(SCRIPT) "$$@"' >> $(WRAPPER_SCRIPT)
	@chmod +x $(WRAPPER_SCRIPT)
	@echo "Wrapper script created: $(WRAPPER_SCRIPT)"

# Ensure LOCAL_BIN_DIR is in PATH (for macOS using zsh)
check-path:
	@if ! echo $$PATH | grep -q "$(LOCAL_BIN_DIR)"; then \
		if [[ $$SHELL == */zsh ]]; then \
		    echo 'export PATH=$$PATH:$(LOCAL_BIN_DIR)' >> ~/.zshrc; \
		    echo "Added $(LOCAL_BIN_DIR) to PATH in ~/.zshrc. Please run 'source ~/.zshrc' or restart your terminal."; \
		elif [[ $$SHELL == */bash ]]; then \
		    echo 'export PATH=$$PATH:$(LOCAL_BIN_DIR)' >> ~/.bashrc; \
		    echo "Added $(LOCAL_BIN_DIR) to PATH in ~/.bashrc. Please run 'source ~/.bashrc' or restart your terminal."; \
		else \
		    echo "Unable to determine shell type. Please manually add $(LOCAL_BIN_DIR) to your PATH."; \
		fi \
	fi

# Clean target: Remove the virtual environment and wrapper script
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_DIR)
	rm -f $(WRAPPER_SCRIPT)

# Uninstall target: Clean up and remove any installed files
uninstall: clean
	@echo "Uninstallation complete."

# Update the tool by pulling the latest changes and reinstalling
update:
	@echo "Pulling the latest changes from the repository..."
	git pull origin main
	@echo "Reinstalling the tool..."
	make clean
	make install
	@echo "Update complete. Tool is up-to-date."

# Help target: Display help message
help:
	@echo "Usage:"
	@echo "  make install       Install the tool"
	@echo "  make clean         Remove the virtual environment and wrapper script"
	@echo "  make uninstall     Clean up and remove installed files"
	@echo "  make update        Pull the latest changes and reinstall"
	@echo "  make help          Display this help message"

.PHONY: install clean uninstall update check-path install-dependencies create-wrapper run help
