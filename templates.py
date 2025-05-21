from langchain.prompts import PromptTemplate
from langchain.prompts.pipeline import PipelinePromptTemplate


introduction = PromptTemplate.from_template("""
You are a jira ticket generator. You will be provided with an issue description and you need to create a jira ticket in the proper format.
""")

create_jira_ticket_template = PromptTemplate.from_template("""
Please create a jira {ticket_type} in the project {project} for the following issue:
{issue_description}
""")

format_jira_ticket_template = PromptTemplate.from_template("""
Please use yaml format and include the following fields in the jira ticket:
- summary - which is a short description of the issue
- description - which is a detailed description of the issue
- issuetype - which is the type of the issue (e.g. bug, task, story)
- epicLink - which is the link to the epic if applicable
- assignee - the person assigned to the issue if not empty
- priority - the priority of the issue from the following options: Normal, Major, Critical
- storyPoints - the story points for the issue if applicable

if you are missing any of the above fields, please omit the field in the output.
Please do not include any other fields in the output.
""")

jira_ticket_example_template = PromptTemplate.from_template("""
Here is an example of a jira ticket in yaml format:

project_key: "myproject"
issues:
  - summary: "convert reboot test to run in ansible"
    description: |
      Convert the reboot test to run in new ansible testing plugin.
    issuetype: "Story"
    epicLink: "myproject-1234"
    assignee: "eshulman"
    priority: "Normal"
    storyPoints: 3
""")

full_template = PromptTemplate.from_template("""
{introduction}

{format}

{example}

{create}
""")

input_prompt = [
    ("introduction", introduction),
    ("format", format_jira_ticket_template),
    ("example", jira_ticket_example_template),
    ("create", create_jira_ticket_template)
]

pipeline_prompt = PipelinePromptTemplate(final_prompt=full_template, pipeline_prompts=input_prompt)
