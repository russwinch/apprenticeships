import json
import sys


def load_json_file(filepath):
    """Opens a json file and converts it to python object."""
    with open(filepath, mode='r') as f:
        apprenticeship_dict = json.load(f)
    return apprenticeship_dict


def output_json_file(*, data, filepath):
    """Converts a python object to json and writes the file."""
    with open(filepath, mode='w') as f:
        json.dump(data, f)


def match_apps(file_a, file_b):
    """
    Compares 2 objects containing apprenticeships and matches them on either
    composite key or the url on the IfA site.

    :file_a: python object containing apprenticeship data
    :file_b: python object containing apprenticeship data

    The composite key is created using the using the name and the level number.
    The expected data files are from the Institute for Apprenticeships and
    Find Apprenticeships Training, but others with a name, level and links to
    the IfA site should work.
    """
    matches = {}
    match_count = 0
    for a in file_a:
        # add create_key function
        a_key = f"{a['name']}: {a['level']}".lower()
        for b in file_b:
            b_key = f"{b['name']}: {b['level']}".lower()
            if a_key == b_key or a['ifa_url'] == b['ifa_url']:
                # we have a match!
                match_count += 1
                matches[a_key] = b_key
    matches['total'] = match_count
    output_json_file(data=matches, filepath='step2a.json')
    print(f"Total matches: {match_count}")


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
