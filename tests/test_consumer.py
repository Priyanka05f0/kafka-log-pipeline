import sys
import os

sys.path.append(os.path.abspath("src/consumer"))

from consumer import should_process_log


def test_valid_error_log():
    log = {"level": "ERROR"}
    assert should_process_log(log, ["ERROR", "WARN"]) is True


def test_valid_warn_log():
    log = {"level": "WARN"}
    assert should_process_log(log, ["ERROR", "WARN"]) is True


def test_info_log_should_fail():
    log = {"level": "INFO"}
    assert should_process_log(log, ["ERROR", "WARN"]) is False


def test_invalid_log_format():
    log = "invalid"
    assert should_process_log(log, ["ERROR", "WARN"]) is False