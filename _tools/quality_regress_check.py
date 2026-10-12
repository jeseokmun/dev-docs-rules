#!/usr/bin/env python3
"""Compatibility entry point for the shared package regression checks."""
from docs_common import cli
from regress_docs_pipeline import main

if __name__ == "__main__":
    raise SystemExit(cli(lambda: main("quality_regress_check")))