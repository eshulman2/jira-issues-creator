#!/usr/bin/env python3
'''
jira_issues_creator.py

This tool interacts with the Jira API to create epics and issues based on configuration files.

It loads configuration details from a YAML file, including Jira connection settings, epics to create,
and issues to be associated with those epics. It utilizes the `jira_handler` module for API interactions.

The script provides the following functionalities:
- Handling of Jira API authentication and request errors.
- Creation of Jira epics and their associated issues.
'''

import argparse
import jira_handler
import logging
import sys
from config_utils import setup_logging, load_yaml_file, get_config_file_path

APP_NAME = 'jira-issues-creator'
DEFAULT_CONFIG_FILE = 'jira_config.yaml'


def main():
    # Set the Python command-line parser and setup the arguments
    parser = argparse.ArgumentParser(prog=APP_NAME,
                                     description='This tool interacts with the Jira API to create epics and issues based on configuration files.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # Required arguments
    parser.add_argument('-l', '--issues_list_file',
                        required=True,
                        help=('YAML file containing the list of Jira epics and issues to create.'))
    # Optional arguments
    parser.add_argument('-c', '--jira_config_file',
                        default=get_config_file_path(default_config_file=DEFAULT_CONFIG_FILE),
                        help=('YAML file containing Jira configuration.'))
    parser.add_argument('--debug',
                        action='store_true',
                        help=('Enable debug-level logging for more detailed output.'))
    # Parse arguments
    parsed_args = parser.parse_args()

    # Set the logging level based on parsed_args.debug
    log_level = logging.DEBUG if parsed_args.debug else logging.INFO
    setup_logging(level=log_level)

    try:
        jira_config_file = get_config_file_path(parsed_args.jira_config_file,
                                                DEFAULT_CONFIG_FILE)
        logging.info(f'Loading Jira configuration from "{jira_config_file}"')
        jira_config = load_yaml_file(jira_config_file)

        logging.debug('Initializing Jira instance based on the configuration')
        jira = jira_handler.Jira(jira_url=jira_config['jira_url'],
                                 jira_api_base_url=jira_config['jira_api_base_url'],
                                 jira_token=jira_config['jira_token'],
                                 jira_special_fields=jira_config['jira_special_fields'])

        issues_list_file = get_config_file_path(config_file=parsed_args.issues_list_file)
        logging.info(
            f'Loading the list of Epics and Issues to create from "{issues_list_file}"')
        issues_list = load_yaml_file(issues_list_file)

        # Load the Jira project key
        if 'project_key' not in issues_list:
            raise KeyError('project_key')
        project_key = issues_list['project_key']

        if 'epics' in issues_list:
            logging.debug(
                f'Creating Epics and associated Issues in the "{project_key}" project')
            jira.create_epics_and_issues(project_key, issues_list['epics'])

        if 'issues' in issues_list:
            logging.debug(f'Creating Issues in the "{project_key}" project')
            jira.create_list_of_jira_issues(project_key, issues_list['issues'])

    except KeyError as e:
        logging.error(
            f'Missing required key "{e}" in "{parsed_args.issues_list_file}"')
        sys.exit(1)
    except Exception as e:
        logging.error(f'An unexpected error occurred: {e}')
        sys.exit(1)


if __name__ == "__main__":
    main()
