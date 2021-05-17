#!/usr/bin/env python

import json
import os
import sys
from collections import defaultdict

import frontmatter
import yaml

ANNOTATIONS_DIR = os.path.join(os.path.dirname(__file__), "..", "annotations")

data = {}  # defaultdict(lambda: )

apps = os.listdir(ANNOTATIONS_DIR)
for app in apps:
    app_dir = os.path.join(ANNOTATIONS_DIR, app)
    valid_labels = []
    try:
        metadata = yaml.load(open(os.path.join(app_dir, "metadata.yaml")))
        data[app] = metadata
        valid_labels = metadata.get("labels", []).keys()
    except:
        data[app] = {}
        pass
    data[app]["annotations"] = defaultdict(lambda: {})
    for annotation_type in ("metrics", "pings"):
        annotation_dir = os.path.join(app_dir, annotation_type)
        if not os.path.isdir(annotation_dir):
            # for some apps, we may have annotations for one annotation type
            # but not another
            continue
        annotation_ids = os.listdir(annotation_dir)
        for annotation_id in annotation_ids:
            annotation_filename = os.path.join(
                annotation_dir, annotation_id, "README.md"
            )
            annotation_md = frontmatter.load(annotation_filename)
            annotation = {"content": annotation_md.content}
            labels = annotation_md.get("labels")
            if labels:
                invalid_labels = [
                    label for label in labels if label not in valid_labels
                ]
                if invalid_labels:
                    sys.stderr.write(
                        f"Invalid labels found in {annotation_filename}: {invalid_labels}"
                    )
                    sys.exit(1)

                annotation.update({"labels": labels})
            data[app]["annotations"][annotation_type][annotation_id] = annotation

print(json.dumps(data))
