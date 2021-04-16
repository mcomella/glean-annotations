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
    valid_components = []
    try:
        metadata = yaml.load(open(os.path.join(app_dir, "metadata.yaml")))
        data[app] = metadata
        valid_components = metadata.get("components", [])
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
            components = annotation_md.get("components")
            if components:
                invalid_components = [
                    component not in valid_components for component in components
                ]
                if invalid_components:
                    sys.stderr.write(
                        f"Invalid components found in {annotation_filename}: {invalid_components}"
                    )
                    sys.exit(1)

                annotation.update({"components": components})
            data[app]["annotations"][annotation_type][annotation_id] = annotation

print(json.dumps(data))
