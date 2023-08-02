"""Script to get the work log for the day."""
# import datetime
import requests


with open("jirapay\jira_api_token.txt", "r", encoding="utf-8") as f:
    API_TOKEN = f.read().strip()


def get_worklogs_for_today():
    """Gets all worklogs for the current user for today."""
    url = "https://cadastra.atlassian.net/jira/rest/api/3/worklog"
    payload = {
        "jql": "worklogDate > 'today' AND author = currentUser()",
        "startAt": 0,
        "maxResults": 100,
    }
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    timeout = 10
    response = requests.get(url, params=payload,
                            headers=headers, timeout=timeout)
    if response.status_code == 200:
        worklogs = response.json()["worklogs"]
        return worklogs

    print(f"Error getting worklogs: {response.status_code}")


def summarize_hours_worked():
    """Summarizes the hours worked in the day at the time of the execution."""
    # today = datetime.datetime.today()
    worklogs = get_worklogs_for_today()
    total_hours = 0
    for worklog in worklogs:
        hours = worklog["timeSpentSeconds"] / 3600
        total_hours += hours
    print(f"Total hours worked today: {total_hours}")


if __name__ == "__main__":
    summarize_hours_worked()
