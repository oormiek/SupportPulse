def analyze_log(log_text):
    """Count common application-support events in a log."""
    lines = log_text.lower().splitlines()

    return {
        "errors": sum("error" in line for line in lines),
        "warnings": sum("warn" in line for line in lines),
        "http_500": sum("http 500" in line for line in lines),
        "timeouts": sum("timeout" in line for line in lines),
        "auth_failures": sum(
            "authentication failure" in line or "unauthorized" in line
            for line in lines
        ),
    }


def classify_issues(stats, log_text):
    """Use simple support rules to classify the most likely issue."""
    text = log_text.lower()

    if stats["timeouts"] and "database" in text:
        return {
            "issue": "Database Connectivity / Performance",
            "priority": "HIGH",
            "recommendations": [
                "Check database availability.",
                "Review database connection pool settings.",
                "Review recent SQL/database errors.",
                "Verify application-to-database connectivity.",
            ],
        }

    if stats["http_500"] and "nullpointerexception" in text:
        return {
            "issue": "Application Error",
            "priority": "HIGH",
            "recommendations": [
                "Review the application stack trace.",
                "Identify the failing service or method.",
                "Check recent application changes.",
                "Retest the affected API after the fix.",
            ],
        }

    if stats["auth_failures"]:
        return {
            "issue": "Authentication / Authorization",
            "priority": "MEDIUM",
            "recommendations": [
                "Verify credentials or tokens.",
                "Check user permissions.",
                "Review authentication service logs.",
                "Confirm the API security configuration.",
            ],
        }

    if "response time" in text:
        return {
            "issue": "Application Performance",
            "priority": "MEDIUM",
            "recommendations": [
                "Measure API response time.",
                "Review slow database operations.",
                "Check CPU and memory utilization.",
                "Look for recent configuration or code changes.",
            ],
        }

    return {
        "issue": "No significant issue detected",
        "priority": "LOW",
        "recommendations": [
            "Continue monitoring the application.",
            "Review logs if the problem reoccurs.",
        ],
    }
