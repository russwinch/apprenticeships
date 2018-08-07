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
    matches = {}
    match_count = 0
    for a in file_a:
        a_key = composite_key(a)
        for b in file_b:
            b_key = composite_key(b)
            if a_key == b_key or a['ifa_url'] == b['ifa_url']:
                # we have a match!
                match_count += 1
                matches[a_key] = b_key

    matches['total'] = match_count
    output_json_file(data=matches, filepath='step2a.json')
    print(f"Total matches: {match_count}")


def dedupe():
    pass
    # 1. iterate through each field in the match from file a, looking for a match in fileb
    # 2. if there is a match then compare the fields and keep the longest one
    #       strings- the longest one
    #       ints - ??
    # 3. for fields which are not in filea, copy them across from fileb
    # 4. flag the record in fileb for deletion (deleting here will mess up the iteration)
    # 5. run through the list of matches from file b and delete them all
    # 6. copy all remaining items from file b into file a
    # 7. output to json


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
