import json
import sys


def load_json_file(filepath):
    """Opens a json file and converts it to python object."""
    with open(filepath, mode='r') as f:
        apprenticeship_dict = json.load(f)
    return apprenticeship_dict


def output_json_file(data, filepath):
    """Converts a python object to json and writes the file."""
    with open(filepath, mode='w') as f:
        json.dump(data, f)


def composite_key(data):
    """Creates a composite key from the name and level."""
    return f"{data['name']}: {data['level']}".lower()


def match_apps(file_a, file_b):
    """
    Compares 2 objects containing apprenticeships and matches them on either
    composite key or the url on the IfA site.

    :file_a: python object containing apprenticeship data
    :file_b: python object containing apprenticeship data

    The expected data files are from the Institute for Apprenticeships and
    Find Apprenticeships Training, but others with a name, level and links to
    the IfA site should work.
    """
    original_b_len = len(file_b)
    matches = {}
    total_matches = 0

    deduped_apprenticeships = []
    file_b_to_remove = []
    total_merged = 0
    for a in file_a:
        a_key = composite_key(a)
        for index, b in enumerate(file_b):
            b_key = composite_key(b)
            if a_key == b_key or a['ifa_url'] == b['ifa_url']:
                # we have a match!
                total_matches += 1
                matches[a_key] = b_key

                a, merged_count = merge_dedupe(a, b)
                total_merged += merged_count
                file_b_to_remove.append(index)
        deduped_apprenticeships.append(a)

    # remove apprenticeships from file_b that have been merged with file_a
    file_b_to_remove.sort(reverse=True)  # delete from the highest index first
    for b in file_b_to_remove:
        del file_b[b]

    # append the remaining unmatched apprenticeships from file_b
    for b in file_b:
        deduped_apprenticeships.append(b)

    matches['total'] = total_matches
    output_json_file(data=matches, filepath='step2a.json')

    print(f"Original file a: {len(file_a)} | file b: {original_b_len}")
    print(f"Total matches: {total_matches}")
    print(f"Deduplicated file: {len(deduped_apprenticeships)}")
    print(f"Total merged fields: {total_merged}")
    return deduped_apprenticeships


def merge_dedupe(match_a, match_b):
    """
    Merges two dictionaries.

    :match_a: a dictionary of apprenticeship data
    :match_b: a dictionary of apprenticeship data

    Preference is given to match_a where there is data in the same field in both
    files.
    """
    merged_field_count = 0

    for key, b_value in match_b.items():
        a_value = match_a.get(key)
        if key == 'source':
            match_a['source'].extend(b_value)  # show the record has been merged
        elif b_value and not a_value:
            match_a[key] = b_value
            merged_field_count += 1

    return match_a, merged_field_count


if __name__ == '__main__':
    ifa_file = 'step1a.json'
    findapp_file = 'step1b.json'

    ifa = load_json_file(ifa_file)
    finda = load_json_file(findapp_file)

    deduped = match_apps(ifa, finda)
    output_json_file(data=deduped, filepath='step2b.json')
