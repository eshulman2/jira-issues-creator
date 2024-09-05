# Example Configuration Files for Jira Issues Creator

## Jira Configuration (`jira_config.yaml`)

The `jira_config.yaml` file contains settings required for interacting with the Jira API. It includes the Jira URL, API base URL, authentication token, and field mappings. Below are the main sections and their explanations:

### Jira Instance Settings

- **`jira_url`**: The base URL of your Jira instance. Replace `https://issues.redhat.com` with your actual Jira URL.
  
- **`jira_api_base_url`**: The base URL for Jira API requests. By default, it is set to `rest/api/2`, which is standard for Jira Cloud API v2. Change it if your Jira instance uses a different API base URL.
  
- **`jira_token`**: Your API token for authenticating requests to Jira. You can obtain this token from your Jira account settings. Replace `<your_jira_api_token>` with your actual API token.

### Jira Special Fields

This section defines mappings and formats for various Jira issue fields:

- **`custom_field_mapping`**: A dictionary mapping specific field names to their corresponding Jira custom field IDs. This mapping is crucial for correctly identifying and updating custom fields in Jira issues.
  
- **`key_format_fields`**: A list of fields that should use the "key" format when creating or updating issues. These fields typically correspond to unique identifiers within Jira, such as components, fix versions, and labels.
  
- **`name_format_fields`**: A list of fields that should use the "name" format when creating or updating issues. These fields are typically user-friendly identifiers, such as assignee, issue type, priority, etc.
  
- **`post_creation_update_fields`**: A list of fields that should be updated post-issue creation. This ensures that necessary updates are made to newly created issues, such as issue links, story points, sprint, status, etc.

### Example Configuration File Link

- (`jira_config.yaml`)

---

## Jira Issues Configuration (`jira_issues.yaml`)

The `jira_issues.yaml` file provides a structured example of Jira issues, demonstrating how to create epics, stories, tasks, and sub-tasks. Below are the main sections and their explanations:

### Jira Project Key

- **`project_key`**: Replace `<YOUR_JIRA_PROJECT_KEY>` with the key of your Jira project where the epics and issues will be created.

### Epics and Issues

#### Epics

- Each epic in the `epics` section defines:
  - **`summary`**: Brief description of the epic.
  - **`epicName`**: The name of the epic in Jira.
  - **`issuetype`**: Issue type for Jira (e.g., Epic).
  - **`description`**: Detailed description of the epic.
  - **`issues`**: Nested list of stories, tasks, and sub-tasks associated with the epic.

#### Standalone Issues

- Each standalone issue in the `issues` section defines:
  - **`summary`**: Brief description of the issue.
  - **`description`**: Detailed description of the issue.
  - **`issuetype`**: Type of the issue (e.g., Story, Task).
  - **`epicLink`**: Key of the epic to which this story will be linked (for standalone issues).
  - **`assignee`**: User assigned to the issue.
  - **`priority`**: Priority level of the issue (e.g., Low, Medium, High).
  - **`issuelinks`**: Links to other issues (e.g., Related, Blocks).

### Example Configuration File Link

- [Download `jira_issues.yaml`](path_to_your_jira_issues.yaml)

---

These configuration files serve as examples for configuring the **Jira Issues Creator** tool. They define how to set up your Jira API connection and structure your project's epics and issues effectively.

---