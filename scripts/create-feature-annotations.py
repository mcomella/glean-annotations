#!/usr/bin/env python

import json
import os
import sys

feature_map = json.load(open(sys.argv[1]))
for metric, features in feature_map.items():
    features = set(features)
    try:
        # the telemetry feature is not what we're tracking
        features.remove("Feature:Telemetry")
    except KeyError:
        pass
    if len(features):
        metric_path = os.path.join("annotations", "fenix", "metrics", metric)
        os.makedirs(metric_path, exist_ok=True)
        open(os.path.join(metric_path, "README.md"), "w").write(
            f"""---
labels: [{", ".join(sorted(features))}]
---

This is a stub commentary for the `{metric}` metric: please feel free to edit (read the
[contributing guidelines](https://github.com/mozilla/glean-annotations/blob/main/CONTRIBUTING.md)
if you haven't done this before)
"""
        )
