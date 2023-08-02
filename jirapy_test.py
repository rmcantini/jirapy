import requests
import json


def test_jira_token():
    """Tests the Jira token API."""
    url = "https://cadastra.atlassian.net/jira/software/c/projects/SCC/boards/36"
    with open("jirapy/jira_api_token.txt", "r", encoding="utf-8") as f:
        token = f.read()
    headers = {"Authorization": "Bearer {}".format(token)}
    timeout = 10
    response = requests.get(url, headers=headers, timeout=timeout)
    if response.status_code == 200:
        return True
    else:
        return False


if __name__ == "__main__":
    if test_jira_token():
        print("The Jira token API is working.")
    else:
        print("The Jira token API is not working.")
