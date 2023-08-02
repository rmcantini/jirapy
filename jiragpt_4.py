'''Script to get all worklogs for the day'''
from datetime import datetime, date, time
from jira import JIRA


# Replace the following variables with your Jira credentials and server URL
JIRA_SERVER = 'https://cadastra.atlassian.net/'
JIRA_USERNAME = 'rcantini@cadastra.com'
API_TOKEN_FILE = 'jirapy/jira_api_token.txt'

# Read the API token from the file
with open(API_TOKEN_FILE, 'r', encoding="utf-8") as file:
    API_TOKEN = file.read().strip()

jira = JIRA(JIRA_SERVER, basic_auth=(JIRA_USERNAME, API_TOKEN))

# Get the current date
current_date = date.today()

# Get the start and end of the day
start_of_day = datetime.combine(current_date, time(9, 0))
end_of_day = datetime.combine(current_date, time(23, 0))

# Construct the JQL query to search for issues with worklogs by your user
# updated within the day
jql_query = f"worklogAuthor = '{JIRA_USERNAME}' \
    AND worklogDate >= startOfDay() AND worklogDate <= endOfDay()"

# Fetch issues based on the JQL query
issues = jira.search_issues(jql_str=jql_query)

TOTAL_TIME_SPENT = 0

# Calculate the total time spent by your user between
# 9 am to 11 pm on the current day
for issue in issues:
    for worklog in issue.fields.worklog.worklogs:
        worklog_date = datetime.strptime(
            worklog.started[:19], "%Y-%m-%dT%H:%M:%S")
        if start_of_day <= worklog_date <= end_of_day:
            TOTAL_TIME_SPENT += worklog.timeSpentSeconds or 0

# Convert the total time spent to hours and minutes
total_hours = TOTAL_TIME_SPENT // 3600
total_minutes = (TOTAL_TIME_SPENT % 3600) // 60

print(
    f"Total Time Spent by {JIRA_USERNAME} on {current_date} between 9 am \
        to 11 pm: {total_hours} hours and {total_minutes} minutes")

print("\nList of Worklogs:")
for idx, issue in enumerate(issues, start=1):
    for worklog in issue.fields.worklog.worklogs:
        worklog_date = datetime.strptime(
            worklog.started[:19], "%Y-%m-%dT%H:%M:%S")
        if start_of_day <= worklog_date <= end_of_day:
            log_date = worklog_date.strftime("%H:%M")
            time_spent = worklog.timeSpentSeconds or 0
            print(
                f"{idx}. Issue Key: {issue.key}, Time Spent: \
                    {time_spent // 3600}h {time_spent % 3600 // 60}m")

print(
    f"\nTotal Time Worked in the Day: \
    {total_hours} hours and {total_minutes} minutes")
