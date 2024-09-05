#!/usr/bin/env python3
'''
config_utils.py

This module provides utility functions for handling configuration files and logging setup.

Functions:
- load_yaml_file(yaml_file): Safely loads and renders YAML configuration files.
   Supports Jinja2 variables template.
- setup_logging(level=logging.INFO): Sets up logging configuration for the application.

Exceptions:
- FileNotFoundError: If the YAML file is not found during loading.
- yaml.YAMLError: If there's an error loading or parsing the YAML file.
- ValueError: If required variables in the YAML content are missing or invalid.
- OSError: If there's an issue creating the logging directory during setup.
- Exception: Any unexpected exception during logging setup.

Dependencies:
- Python modules: os, logging, datetime, yaml, jinja2
'''

from datetime import datetime
import inspect
from jinja2 import Template, Environment, meta
import logging
import os
import yaml


def setup_logging(level=logging.INFO):
    '''
    Set up logging configuration for the application. This function creates a
    logging directory specific to the script, configures file and console handlers,
    and sets the desired logging level.

    Args:
        level (int or str): Logging level to be set. Defaults to logging.INFO.
                            Can be one of:
                            - logging.DEBUG
                            - logging.INFO
                            - logging.WARNING
                            - logging.ERROR
                            - logging.CRITICAL

    Raises:
        OSError: If there's an issue creating the logging directory.
        Exception: Any unexpected exception during logging setup.
    '''
    try:
        # Get the caller's module name
        caller_module = inspect.stack()[1].filename
        script_name = os.path.splitext(os.path.basename(caller_module))[0]

        # Define the logging directory based on the script name
        logging_directory = f'/tmp/{script_name}/'

        # Ensure the logging directory exists
        if not os.path.exists(logging_directory):
            os.makedirs(logging_directory)

        # Create a logging file with a timestamp
        time_format = datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
        logging_file_name = f'{time_format}.log'
        logging_file = os.path.join(logging_directory, logging_file_name)

        # Configure root logger
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s [%(levelname)s] %(message)s')

        # Create file handler to save logs to a file
        file_handler = logging.FileHandler(logging_file)
        file_handler.setLevel(logging.DEBUG)  # Capture DEBUG and above

        # Create console handler for logging to console
        console_handler = logging.StreamHandler()
        # Set console handler to the specified level
        console_handler.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s')

        # Set formatter for handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Clear any existing handlers to avoid duplicate logs
        logging.root.handlers.clear()

        # Add handlers to the root logger
        logging.root.addHandler(file_handler)
        logging.root.addHandler(console_handler)

        logging.info(f'Logging DEBUG execution logs to: {logging_file}')

    except OSError as e:
        # If an error occurs during logging directory creation, log the OSError
        logging.error(f'Failed to create logging directory: {str(e)}')
        raise e
    except Exception as e:
        # If an unexpected error occurs during logging setup, log the exception message
        logging.error(f'Failed to set up logging: {str(e)}')
        raise e


def get_config_file_path(config_file, default_config_file=''):
    """
    Determine the absolute path of a configuration file.

    Args:
    - config_file (str): The provided configuration file path.
    - default_config_file (str): The default configuration file name.

    Returns:
    - str: The absolute path of the configuration file. If `config_file` is
           equal to `default_config_file`, the path is determined relative to
           the directory of the current script. If `config_file` starts with
           '~', it is expanded to the user's home directory. Otherwise,
           `config_file` is returned as an absolute path.

    Note:
    - If `config_file` is a relative path and not equal to `default_config_file`,
      it is returned as an absolute path relative to the current working directory.
    """
    # Determine the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    if config_file == default_config_file:
        return os.path.join(script_dir, default_config_file)
    else:
        expanded_path = os.path.expanduser(config_file)
        return os.path.abspath(expanded_path)


def load_yaml_file(yaml_file):
    '''
    Load YAML configuration file safely and render Jinja2 templates.
    Supports Jinja2 variables template.

    Args:
        yaml_file (str): Path to the YAML file to load.

    Returns:
        dict: Loaded and rendered YAML content as a dictionary.

    Raises:
        FileNotFoundError: If the YAML file is not found.
        yaml.YAMLError: If there's an error loading the YAML file.
        ValueError: If required variables are missing or invalid.
    '''

    def extract_template_variables(template_content):
        '''
        Extract the required variables from a Jinja2 template.

        Args:
            template_content (str): The content of the Jinja2 template.

        Returns:
            set: A set of variable names required by the template.
        '''
        env = Environment()
        parsed_content = env.parse(template_content)
        return meta.find_undeclared_variables(parsed_content)

    try:
        with open(yaml_file, 'r') as file:
            yaml_content = file.read()

        # First pass: Load YAML to extract variables if present
        initial_load = yaml.safe_load(yaml_content)

        # Check if there are any template variables in the YAML content
        required_variables = extract_template_variables(yaml_content)

        if required_variables:
            # Render Jinja2 template with extracted variables if needed
            template = Template(yaml_content)
            variables = initial_load if isinstance(initial_load, dict) else {}
            rendered_content = template.render(variables)
        else:
            rendered_content = yaml_content

        # Second pass: Load YAML from rendered content safely
        loaded_file = yaml.safe_load(rendered_content)
    except FileNotFoundError as exc:
        logging.error(f'Failed to find the YAML file "{yaml_file}"')
        raise exc
    except yaml.YAMLError as exc:
        logging.error(
            f'Failed to load the YAML file "{yaml_file}": {exc}')
        raise exc
    except ValueError as exc:
        logging.error(f'Validation error: {exc}')
        raise exc
    except Exception as exc:
        logging.error(f'An unexpected error occurred: {exc}')
        raise exc
    return loaded_file
