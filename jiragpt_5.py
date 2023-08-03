from jira import JIRA
from datetime import datetime, date, time

# Replace the following variables with your Jira credentials and server URL
JIRA_SERVER = 'https://cadastra.atlassian.net/'
JIRA_USERNAME = 'rcantini@cadastra.com'
API_TOKEN_FILE = r'jirapay\jira_api_token.txt'

# Read the API token from the file
with open(API_TOKEN_FILE, 'r', encoding="utf-8") as file:
    API_TOKEN = file.read().strip()

jira = JIRA(JIRA_SERVER, basic_auth=(JIRA_USERNAME, API_TOKEN))

# Get the current date
current_date = date.today()

# Get the start and end of the day
start_of_day = datetime.combine(current_date, time(9, 0))
end_of_day = datetime.combine(current_date, time(23, 0))

# Construct the JQL query to search for issues with worklogs created by your user within the day
jql_query = (
    f"worklogAuthor = '{JIRA_USERNAME}' AND "
    f"worklogDate >= '{start_of_day.strftime('%Y-%m-%d')}' AND "
    f"worklogDate <= '{end_of_day.strftime('%Y-%m-%d')}'"
)

# Fetch issues based on the JQL query
issues = jira.search_issues(jql_str=jql_query)

total_time_spent = 0

# Calculate the total time spent by your user on the current day
for issue in issues:
    for worklog in issue.fields.worklog.worklogs:
        # Check if the worklog belongs to your Jira username and is within the current day
        if worklog.author.displayName == JIRA_USERNAME:
            time_spent = worklog.timeSpentSeconds or 0
            total_time_spent += time_spent

# Convert the total time spent to hours and minutes
total_hours = total_time_spent // 3600
total_minutes = (total_time_spent % 3600) // 60

print(
    f"Total Time Spent by {JIRA_USERNAME} on {current_date}: {total_hours} hours and {total_minutes} minutes")
