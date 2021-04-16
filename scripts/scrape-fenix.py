#!/usr/bin/env python

import json
import os
import re
import sys

import requests


FENIX_METRICS_URL = 'https://probeinfo.telemetry.mozilla.org/glean/fenix/metrics'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

if not GITHUB_TOKEN:
    print("Github token required!")
    sys.exit(1)


fenix_metrics = requests.get(FENIX_METRICS_URL).json()
issue_map = {}
for metric_name, metric in fenix_metrics.items():
    raw_bugs = metric['history'][-1]['bugs']
    fenix_issues = [re.sub(r'.*/issues/([0-9]+)', r'\1', bug) for bug in raw_bugs if 'mozilla-mobile/fenix/issues' in str(bug)]
    if fenix_issues:
        issue_map[metric_name] = fenix_issues

issue_cache = {}
def get_issue(number):
    return requests.get(f"https://api.github.com/repos/mozilla-mobile/fenix/issues/{number}", headers={'Authorization': 'token %s' % GITHUB_TOKEN}).json()

feature_map = {}
for metric, issue_numbers in issue_map.items():
    features = []
    for issue_number in issue_numbers:
        if not issue_cache.get(issue_number):
            print(issue_number)
            issue = get_issue(issue_number)
            label_names = [label['name'] for label in issue['labels'] if label['name'].startswith('Feature:')]
            issue_cache[issue_number] = label_names
        features.extend(issue_cache[issue_number])
    feature_map[metric] = features

print(json.dumps(feature_map))
