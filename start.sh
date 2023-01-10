#!/bin/sh
set -x

# Start scan
gitleaks detect -s /var/src/ --no-git -v -c /opt/gitleaks/config.toml --exit-code=0 -r /var/reports/gitleaks.json

# Parse Report for SEQHUB
python3 /opt/gitleaks/seqhub_report.py

cat /var/reports/seqhub.json
