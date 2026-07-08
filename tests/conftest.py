"""Shared pytest fixtures."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
EVAL_DIR = ROOT / "eval"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(EVAL_DIR) not in sys.path:
    sys.path.insert(0, str(EVAL_DIR))


@pytest.fixture
def tmp_log_dir(tmp_path: Path) -> Path:
    return tmp_path / "logs"
