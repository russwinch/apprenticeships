import json
import sys


def load_json_file(filepath):
    """Opens a json file and converts it to a python object."""
    with open(filepath, mode='r') as f:
        apprenticeship_dict = json.load(f)
    return apprenticeship_dict


def output_json_file(data, filepath):
    """Converts a python object to json and writes to the filepath."""
    with open(filepath, mode='w') as f:
        json.dump(data, f)


def composite_key(data):
    """Creates a composite key from the name and level of a supplied dictionary."""
    return f"{data['name']}: {data['level']}".lower()


def match_apps(file_a, file_b, schema=None):
    """
    Compares 2 objects containing apprenticeships and matches them on either
    composite key or the url on the IfA site.

    :file_a: object containing apprenticeship data
    :file_b: object containing apprenticeship data

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
        a = schema.enforce(a)
        deduped_apprenticeships.append(a)

    # remove apprenticeships from file_b that have already been merged
    file_b_to_remove.sort(reverse=True)  # delete from the highest index first
    for b in file_b_to_remove:
        del file_b[b]

    # append the remaining unmatched apprenticeships from file_b
    for b in file_b:
        b = schema.enforce(b)
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
    Merges two dictionaries and returns the matched dict and the count of merged fields.

    :match_a: a dictionary containing a single apprenticeship
    :match_b: a dictionary containing a single apprenticeship

    Preference is given to match_a where there is data in the same field in both
    files.
    """
    merged_field_count = 0

    for key, b_value in match_b.items():
        a_value = match_a.get(key)
        if key == 'source':
            match_a['source'].extend(b_value)  # show the record has been merged
        elif b_value and not a_value:  # TODO: when b_value is null this line causes the column to be lost
            match_a[key] = b_value
            merged_field_count += 1

    return match_a, merged_field_count


class Schema(object):
    """Holds and enforces the expected fields in the dataset."""
    def __init__(self, apps=None):
        """
        Create an empty schema.

        :apps: python object containing apprenticeships
        """
        self.schema = set()
        if apps:
            self.append(apps)

    def append(self, apps):
        """
        Extract columns from a file and deduplicate by using a set.

        :apps: python object containing apprenticeships

        Useful if the incoming data is not clean and there are discrepancies in columns.
        ***In this scenario it could just be run on the first record, but running against
        all just to be sure and for application against other datasets.***
        """

        fields = set()
        for app in apps:
            for field in app.keys():
                fields.add(field)

        self.schema = self.schema.union(fields)

    def enforce(self, fields):
        """
        Check all fields in a record against a schema and add any missing items.

        :fields: object of apprenticeships
        """
        for s in self.schema:
            try:
                fields[s]
            except KeyError:
                fields[s] = None
        return fields


if __name__ == '__main__':
    ifa_file = 'step1a.json'
    findapp_file = 'step1b.json'

    ifa = load_json_file(ifa_file)
    finda = load_json_file(findapp_file)

    schema = Schema(ifa)
    schema.append(finda)

    deduped = match_apps(ifa, finda, schema=schema)
    output_json_file(data=deduped, filepath='step2b.json')
