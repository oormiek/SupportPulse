from analyzer import analyze_log, classify_issues


def test_database_failure_detection():
    log = """
    ERROR Database connection timeout
    ERROR HTTP 500 returned
    WARN Database response time 3000ms
    """

    stats = analyze_log(log)

    assert stats["errors"] == 2
    assert stats["warnings"] == 1
    assert stats["http_500"] == 1
    assert stats["timeouts"] == 1


def test_database_classification():
    log = "ERROR Database connection timeout"

    stats = analyze_log(log)
    result = classify_issues(stats, log)

    assert result["issue"] == "Database Connectivity / Performance"
    assert result["priority"] == "HIGH"


def test_authentication_classification():
    log = "WARN Authentication failure"

    stats = analyze_log(log)
    result = classify_issues(stats, log)

    assert result["issue"] == "Authentication / Authorization"
