from collections import namedtuple
import pytest

import matching


class TestCompositeKey():
    def test_composite_key_with_lower_case(self):
        test_data = {'name': 'foo', 'level': 'bar'}
        assert matching.composite_key(test_data) == 'foo: bar'

    def test_composite_key_with_upper_case(self):
        test_data = {'name': 'FOO', 'level': 'BAR'}
        assert matching.composite_key(test_data) == 'foo: bar'

    def test_composite_key_with_integers(self):
        test_data = {'name': 1, 'level': 5}
        assert matching.composite_key(test_data) == '1: 5'

    def test_composite_key_with_additional_values(self):
        test_data = {'name': 'test', 'level': 7, 'other': 'stuff', 'more': 'things'}
        assert matching.composite_key(test_data) == 'test: 7'

    def test_composite_key_fails_when_value_missing(self):
        test_data = {'level': 7, 'other': 'stuff', 'more': 'things'}
        with pytest.raises(KeyError):
            matching.composite_key(test_data)


class TestMergeDedupe():
    # setup for these tests
    @staticmethod
    @pytest.fixture
    def test_dicts():
        TestMatching = namedtuple('TestMatching', 'a, b')
        test_data = TestMatching(
                a={'name': 'matching_name',
                   'level': None,
                   'length': '12 months',
                   'a_only_field': 'a_data',
                   'source': ['file_a']
                   },

                b={'name': 'matching_name',
                   'level': 3,
                   'length': None,
                   'b_only_field': 'b_data',
                   'source': ['file_b']
                   }
                )
        return test_data

    def test_count(self, test_dicts):
        _, count = matching.merge_dedupe(test_dicts.a, test_dicts.b)
        assert count == 2  # the two fields containing None

    def test_empty_fields_are_merged(self, test_dicts):
        merged, _ = matching.merge_dedupe(test_dicts.a, test_dicts.b)
        assert merged['level'] == 3
        assert merged['length'] == '12 months'

    def test_missing_fields_are_merged(self, test_dicts):
        merged, _ = matching.merge_dedupe(test_dicts.a, test_dicts.b)
        assert merged.get('b_only_field') == 'b_data'

    def test_sources_are_combined(self, test_dicts):
        merged, _ = matching.merge_dedupe(test_dicts.a, test_dicts.b)
        assert merged['source'] == ['file_a', 'file_b']

    def test_file_a_takes_priority(self, test_dicts):
        # override some values for this test
        test_dicts.a['name'] = 'matching_name_file_a'
        test_dicts.b['name'] = 'matching_name_file_b'

        merged, _ = matching.merge_dedupe(test_dicts.a, test_dicts.b)
        assert merged['name'] == 'matching_name_file_a'


class TestSchema():
    # setup for these tests
    @staticmethod
    @pytest.fixture
    def schema():
        test_data = [{'name': 'foo', 'level': 4, 'length': '12 months'},
                     {'name': 'bar', 'level': 7, 'qualifications': 'many'}
                     ]
        test_schema = matching.Schema(test_data)
        return test_schema

    def test_append_while_init(self, schema):
        assert schema.schema == {'name', 'level', 'length', 'qualifications'}

    def test_append_while_empty(self):
        test_data = [{'name': 'foo', 'level': 4, 'length': '12 months'},
                     {'name': 'bar', 'level': 7, 'qualifications': 'many'}
                     ]
        schema = matching.Schema()
        schema.append(test_data)
        assert schema.schema == {'name', 'level', 'length', 'qualifications'}

    def test_append_to_existing(self, schema):
        more_test_data = [{'level': 9, 'status': 'Approved', 'version': None}]
        schema.append(more_test_data)
        assert schema.schema == {'name', 'level', 'length', 'qualifications', 'status', 'version'}

    def test_enforce_with_missing_fields(self, schema):
        fields = {'level': 9, 'length': '24 months'}
        output = schema.enforce(fields)
        assert output == {'name': None, 'level': 9, 'length': '24 months', 'qualifications': None}

    def test_enforce_when_fields_already_present(self, schema):
        fields = {'name': 'apprentice', 'level': 9, 'length': '24 months', 'qualifications': None}
        output = schema.enforce(fields)
        assert output == {'name': 'apprentice', 'level': 9, 'length': '24 months', 'qualifications': None}

    def test_enforce_ignores_extra_fields_not_in_schema(self, schema):
        fields = {'name': 'apprentice', 'level': 9, 'length': '24 months', 'qualifications': None, 'status': None}
        output = schema.enforce(fields)
        assert output == {'name': 'apprentice', 'level': 9, 'length': '24 months', 'qualifications': None, 'status': None}
