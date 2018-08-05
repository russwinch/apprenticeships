import json


def load_file(filepath):
    """Opens a json file and converts it to python object."""
    with open(filepath, mode='r') as f:
        apprenticeship_dict = json.load(f)
    return apprenticeship_dict


def match_apps(*, ifa, finda):
    """
    Compares 2 objects containing apprenticeships and matches them on either
    composite key or the url on the IfA site.

    The composite key is created using the using the name and the level number.
    :ifa: python object containing data from the Institute for Apprenticeships
    :finda: python object containing data from Find Apprenticeships Training
    """
    match_count = 0
    for a in ifa:
        a_key = f"{a['name']}: {a['level'][:1]}".lower()
        for b in finda:
            b_key = f"{b['name']}: {b['level'][:1]}".lower()
            if a_key == b_key or a['url'] == b['ifa_url']:
                # we have a match!
                match_count += 1
                print(a_key, ":", b_key)
                # TODO: output to JSON here
    print(f"Total matches: {match_count}")


if __name__ == '__main__':
    ifa_file = 'step1a.json'
    findapp_file = 'step1b.json'

    ifa = load_file(ifa_file)
    finda = load_file(findapp_file)

    match_apps(ifa=ifa, finda=finda)
