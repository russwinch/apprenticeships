"""
A collection of scripts that were useful during the project.
"""

import json


def get_ifa_keys(ifa_json_filepath):
    """Produces a deduplicated list of headings scraped from the IfA dataset."""
    with open(ifa_json_filepath) as f:
        ifa = json.load(f)

    headings = set()
    for app in ifa:
        for heading in app.keys():
            headings.add(heading)

    return list(headings)
