"""Smoke tests for package skeleton."""

import anomaly_detection
from anomaly_detection.cli.detect import main


def test_version() -> None:
    assert anomaly_detection.__version__ == "0.1.0"


def test_detect_cli_stub(capsys) -> None:
    main()
    captured = capsys.readouterr()
    assert "not implemented until Phase 3" in captured.out
