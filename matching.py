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
    match_count = 0

    deduped_apprenticeships = []
    file_b_to_remove = []
    fields_deduped_count = 0
    for a in file_a:
        a_key = composite_key(a)
        for index, b in enumerate(file_b):
            b_key = composite_key(b)
            if a_key == b_key or a['ifa_url'] == b['ifa_url']:
                # we have a match!
                match_count += 1
                matches[a_key] = b_key

                a, count = dedupe(a, b)
                fields_deduped_count += count
                file_b_to_remove.append(index)
        deduped_apprenticeships.append(a)

    file_b_to_remove.sort(reverse=True)  # delete from the highest index first
    for b in file_b_to_remove:
        del file_b[b]

    for b in file_b:
        deduped_apprenticeships.append(b)

    matches['total'] = match_count
    output_json_file(data=matches, filepath='step2a.json')
    output_json_file(data=deduped_apprenticeships, filepath='step2b.json')
    print(f"Original file a: {len(file_a)} | File b: {original_b_len}")
    print(f"Total matches: {match_count}")
    print(f"Total deduped fields: {fields_deduped_count}")
    print(f"Deduplicated file: {len(deduped_apprenticeships)}")


def dedupe(match_a, match_b):
    deduped_count = 0
    deduped_item = {}
    for key, a_value in match_a.items():
        b_value = match_b.get(key)
        if b_value and not a_value:
            deduped_item[key] = b_value
            deduped_count += 1
        else:
            deduped_item[key] = a_value

    for key, b_value in match_b.items():
        a_value = match_a.get(key)
        if a_value and not b_value:
            deduped_item[key] = a_value
            deduped_count += 1
        else:
            deduped_item[key] = b_value

    return deduped_item, deduped_count


if __name__ == '__main__':
    ifa_file = 'step1a.json'
    findapp_file = 'step1b.json'

    ifa = load_json_file(ifa_file)
    finda = load_json_file(findapp_file)

    match_apps(ifa, finda)
    try:
        if sys.argv[1] == 'matchonly':
            sys.exit()
    except IndexError:
        # no arguments were passed when the script was called so we can ignore
        pass

    # continue on to the dedupe...
