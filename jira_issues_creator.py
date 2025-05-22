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
import os
from getpass import getpass
from config_utils import get_config_file_path, setup_logging, load_yaml_file
from chat_handler import ChatHandler
from templates import start_prompt, whats_wrong_prompt, create_jira_ticket_template, fix_jira_ticket_template



APP_NAME = 'jira-issues-creator'
DEFAULT_CONFIG_FILE = 'jira_config.yaml'


def main():
    # Set the Python command-line parser and setup the arguments
    parser = argparse.ArgumentParser(prog=APP_NAME,
                                     description='Automates the creation of epics, stories, tasks, and sub-tasks in Jira based on YAML configuration files.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # Required arguments
    parser.add_argument('-p', '--prompt',
                        required=True,
                        help=('prompt describing the issue to create.'))
    parser.add_argument('-t', '--ticket-type',
                        required=True,
                        help=('Type of the ticket to create (e.g., story, epic, etc.).'))
    parser.add_argument('-j', '--jira-project',
                        required=True,
                        help=('Jira project key where the issue will be created.'))

    # Optional arguments
    parser.add_argument('-c', '--config-file',
                        default=get_config_file_path(
                            default_config_file=DEFAULT_CONFIG_FILE),
                        help=('Path to the YAML file containing Jira configuration.'))

    parser.add_argument('--debug',
                        action='store_true',
                        help=('Enable debug-level logging for detailed output.'))
    parser.add_argument('--use-ollama',
                        action='store_true',
                        help=('use local ollama instance instead of openAI.'))
    parser.add_argument('--model-name',
                        default='o4-mini-2025-04-16',
                        help=('Name of the model to use for generating tickets.'))
    # Parse arguments
    parsed_args = parser.parse_args()

    log_level = logging.DEBUG if parsed_args.debug else logging.INFO
    setup_logging(level=log_level)

    jira_config_file = get_config_file_path(parsed_args.config_file)
    logging.info(f'Loading configuration from "{jira_config_file}"')
    jira_config = load_yaml_file(jira_config_file)

    if not parsed_args.use_ollama:
        # Set the OpenAI API key environment variable
        os.environ["OPENAI_API_KEY"] = getpass("Enter Your OpenAI API Key: ")

    chat = ChatHandler(model_name=parsed_args.model_name,
                       ollama=parsed_args.use_ollama)

    satisfied = False
    user_prompt = parsed_args.prompt
    prompt = start_prompt
    history_template = create_jira_ticket_template
    while not satisfied:
        response = chat.invoke_chain({"ticket_type": parsed_args.ticket_type,
                                      "issue_description": user_prompt,
                                      "project": parsed_args.jira_project},
                                     prompt,
                                     history_template)
        validation = input(f"Please review the generated ticket:\n{response.content}\n\nAre you satisfied with the ticket? [y/n]: ")
        if validation.lower() == "y":
            satisfied = True
        else:
            print("Let's try again.")
            prompt = whats_wrong_prompt
            history_template = fix_jira_ticket_template
            user_prompt = input("What changes would you like me to make? : ")

    logging.debug('Initializing Jira instance based on the configuration')
    jira = jira_handler.Jira(jira_url=jira_config['jira_url'],
                             jira_api_base_url=jira_config['jira_api_base_url'],
                             jira_token=jira_config['jira_token'],
                             jira_special_fields=jira_config['jira_special_fields'])

    jira.jira_issues_creator(response.content)


if __name__ == "__main__":
    main()
