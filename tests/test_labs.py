import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "labs", "python"))

import health_checker  # noqa: E402
import log_analyzer  # noqa: E402
import system_report  # noqa: E402

DATA = os.path.join(os.path.dirname(__file__), "..", "labs", "data", "access.log")


def test_parse_line_valid():
    line = '10.0.0.5 - - [10/Nov/2026:10:00:01 +0000] "GET /health HTTP/1.1" 200 15 "-" "curl/8.5"'
    entry = log_analyzer.parse_line(line)
    assert entry["ip"] == "10.0.0.5"
    assert entry["path"] == "/health"
    assert entry["status"] == 200
    assert entry["size"] == 15


def test_parse_line_invalid_returns_none():
    assert log_analyzer.parse_line("this is not a log line") is None


def test_analyse_sample_log():
    with open(DATA, encoding="utf-8") as handle:
        report = log_analyzer.analyse(handle, top=3)
    assert report["total_requests"] == 20
    assert report["malformed_lines"] == 0
    assert report["status_counts"][500] == 2
    assert report["status_counts"][503] == 1
    assert report["error_rate_5xx"] == 0.15
    assert report["top_ips"][0][0] in {"10.0.0.5", "10.0.0.9", "10.0.0.12"}


def test_analyse_counts_malformed_and_skips_blank():
    report = log_analyzer.analyse(["", "garbage", "also bad"])
    assert report["total_requests"] == 0
    assert report["malformed_lines"] == 2
    assert report["error_rate_5xx"] == 0.0


def test_log_analyzer_cli_missing_file(capsys):
    assert log_analyzer.main(["/no/such/file.log"]) == 2
    assert "cannot read" in capsys.readouterr().err


def test_health_checker_bad_url_is_failure():
    result = health_checker.check("not-a-valid-url", timeout=1)
    assert result.ok is False
    assert result.status is None


def test_system_report_has_expected_keys():
    report = system_report.build_report()
    assert {"hostname", "os", "python", "cpu_count", "disk"} <= report.keys()
