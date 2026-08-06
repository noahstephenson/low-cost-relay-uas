#!/usr/bin/env python3
"""Run the baseline ID, preservation, duplicate, and reference checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


validator = Path(__file__).with_name("validate-baseline.py")
result = subprocess.run([sys.executable, str(validator), "--ids-only"], check=False)
sys.exit(result.returncode)
