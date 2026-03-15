def create_plan(issue):

    title = issue["title"]
    body = issue["body"]

    print("\nPlanning solution for issue:", title)
    print("-"*40)

    plan = []

    if "bug" in title.lower():
        plan = [
            "Locate the code related to the bug",
            "Reproduce the issue",
            "Identify the faulty logic",
            "Implement the fix",
            "Test the fix"
        ]

    elif "security" in title.lower():
        plan = [
            "Locate the logging system",
            "Identify where PII data is printed",
            "Implement data masking",
            "Add tests for masked output",
            "Verify compliance rules"
        ]

    elif "task" in title.lower():
        plan = [
            "Understand task requirements",
            "Identify affected components",
            "Implement required changes",
            "Test functionality",
            "Document the changes"
        ]

    else:
        plan = [
            "Analyze issue",
            "Find related code",
            "Implement solution",
            "Test fix"
        ]

    for step in plan:
        print("Step:", step)

    return plan