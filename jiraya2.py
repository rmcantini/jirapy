def summarize_hours_worked():
    """Summarizes the hours worked in the day at the time of the execution."""
    today = datetime.datetime.today()
    worklogs = get_worklogs_for_today()
    if worklogs is None:
        print("No worklogs found")
        return
    total_hours = 0
    for worklog in worklogs:
        hours = worklog["timeSpentSeconds"] / 3600
        total_hours += hours
    print(f"Total hours worked today: {total_hours}")


if __name__ == "__main__":
    summarize_hours_worked()
