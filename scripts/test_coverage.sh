#!/bin/bash
# run unittests with coverage.py
python -m pytest --cov=mlbgame --cov-report html:../mlbgame/cov_html ../mlbgame/tests/

# open coverage report in default browser
open ../mlbgame/cov_html/index.html