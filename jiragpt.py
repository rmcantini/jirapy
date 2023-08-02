from jira import JIRA
from datetime import datetime, date

# Replace the following variables with your Jira credentials and server URL
JIRA_SERVER = 'https://cadastra.atlassian.net/'
JIRA_USERNAME = 'rcantini@cadastra.com'
# Path to the file containing the API token
API_TOKEN_FILE = 'jirapy/jira_api_token.txt'

# Read the API token from the file
with open(API_TOKEN_FILE, 'r', encoding="utf-8") as file:
    API_TOKEN = file.read().strip()

jira = JIRA(JIRA_SERVER, basic_auth=(JIRA_USERNAME, API_TOKEN))

# Get the current date
current_date = date.today()

# Get the start and end of the day
start_of_day = datetime.combine(current_date, datetime.min.time())
end_of_day = datetime.combine(current_date, datetime.max.time())

# Construct the JQL query to search for issues with worklogs updated within the day
jql_query = f"worklogDate >= startOfDay() AND worklogDate <= endOfDay()"

# Fetch issues based on the JQL query
issues = jira.search_issues(jql_str=jql_query)

# Loop through the issues and print relevant information
for issue in issues:
    print("Issue Key:", issue.key)
    print("Summary:", issue.fields.summary)
    print("Assignee:", issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned")
    print("Time Spent:", issue.fields.timespent)
    print("----------")
