import os
from cluedin import cluedin

from jqqb_evaluator.evaluator import Evaluator

from json import dump

from dotenv import load_dotenv
load_dotenv()


class TestCluedIn:
    def test_get_a_token(self):
        # Arrange
        username = os.environ.get('USER')
        password = os.environ.get('PASSWORD')
        org_name = os.environ.get('ORGANIZATION')
        auth_url = os.environ.get('AUTH_URL')
        # Act
        token = cluedin.get_token(username, password, org_name, auth_url)
        # Assert
        assert len(token) > 2000

    def test_search(self):
        # Arrange
        username = os.environ.get('USER')
        password = os.environ.get('PASSWORD')
        org_name = os.environ.get('ORGANIZATION')
        auth_url = os.environ.get('AUTH_URL')
        api_url = os.environ.get('API_URL')
        token = cluedin.get_token(username, password, org_name, auth_url)
        # Act
        result = cluedin.search(
            token, api_url, query="*", entries=['id', 'name'])
        # Assert
        assert len(result['data']['search']['entries']) == 20

    def test_rule_operator_id_to_querybuilder_string(self):
        assert cluedin.rule_operator_id_to_querybuilder_string(
            '0bafc522-8011-43ba-978a-babe222ba466') == 'equal'

    def test_rule_json_to_querybuilder(self):
        # Arrange
        rule_json = {
          'id': '8a479e5b-919f-4aa7-9862-1045b6eaedcf',
          'name': 'Death Year',
          "description": "[{\"type\":\"paragraph\",\"children\":[{\"text\":\"Delete the IMDb.name.basic.DeathYear value if it equals to \\\\N \"}]}]",
          'organizationId': '0130ffc7-e435-4a28-8d57-7f236c339277',
          'type': 'ProcessingRule',
          'order': 1,
          'createdBy': 'cd42615b-5552-4244-a97f-a9ae4f214133',
          'createdAt': '2022-02-14T12:04:45.4522443+00:00',
          'modifiedBy': 'cd42615b-5552-4244-a97f-a9ae4f214133',
          'modifiedAt': '2022-02-14T12:06:45.909032+00:00',
          'isActive': True,
          'ownedBy': 'cd42615b-5552-4244-a97f-a9ae4f214133',
          'conditions': {
            'objectTypeId': '00000000-0000-0000-0000-000000000000',
            'condition': 'AND',
            'field': None,
            'id': '27fd6a61-3439-484d-be8a-49444186728a',
            'operator': '00000000-0000-0000-0000-000000000000',
            'rules': [
              {
                'objectTypeId': '011ac3b4-0b46-4f9c-a82a-8c14f9dd642b', # vocabulary
                'condition': 'AND',
                'field': 'Properties[IMDb.name.basic.DeathYear]',
                'id': 'e48f2041-d981-4b61-a611-aa3c8d508e1e',
                'operator': '0bafc522-8011-43ba-978a-babe222ba466',
                'rules': [],
                'type': 'string',
                'value': [
                  '\\N'
                ]
              }
            ],
            'type': None,
            'value': None
          },
          'actions': [
            {
              'name': 'Delete Value',
              'supportsPreview': False,
              'properties': [
                {
                  'name': 'FieldName',
                  'type': 'System.String',
                  'friendlyType': None,
                  'friendlyName': None,
                  'value': 'IMDb.name.basic.DeathYear'
                }
              ],
              'type': 'CluedIn.Rules.Actions.DeleteValue, CluedIn.Rules, Version=3.2.0.0, Culture=neutral, PublicKeyToken=null'
            }
          ]
        }

        expected_querybuilder_json = { # WIP
          'condition': 'AND',
          'rules': [
            {
              'id': 'todo',
              'field': 'Properties[IMDb.name.basic.DeathYear]',
              'type': 'string',
              'input': 'text',
              'operator': 'equal',
              'value': '\\N'
            }
          ]
        }
        # Act
        result = cluedin.rule_json_to_querybuilder(rule_json)
        # Assert
        assert dump(result) == dump(expected_querybuilder_json)

    def test_run_rules(self):
        # Arrange
        rule_id = '8a479e5b-919f-4aa7-9862-1045b6eaedcf'
        username = os.environ.get('USER')
        password = os.environ.get('PASSWORD')
        org_name = os.environ.get('ORGANIZATION')
        auth_url = os.environ.get('AUTH_URL')
        api_url = os.environ.get('API_URL')
        token = cluedin.get_token(username, password, org_name, auth_url)
        # Act
        rule = cluedin.get_rule(token, api_url, rule_id)

        # expected:
        # "condition": "AND",
        # "rules": [{
        #     "id": "tagname",
        #     "field": "tags.name",
        #     "type": "string",
        #     "input": "text",
        #     "operator": "not_contains",
        #     "value": "production"
        # }, {
        #     "id": "tagname",
        #     "field": "tags.name",
        #     "type": "string",
        #     "input": "text",
        #     "operator": "begins_with",
        #     "value": "development"
        # },

        # actual:
        # "conditions": {
        #     "objectTypeId": "00000000-0000-0000-0000-000000000000",
        #     "condition": "AND",
        #     "field": null,
        #     "id": "27fd6a61-3439-484d-be8a-49444186728a",
        #     "operator": "00000000-0000-0000-0000-000000000000",
        #     "rules": [
        #         {
        #             "objectTypeId": "011ac3b4-0b46-4f9c-a82a-8c14f9dd642b",
        #             "condition": "AND",
        #             "field": "Properties[IMDb.name.basic.DeathYear]",
        #             "id": "e48f2041-d981-4b61-a611-aa3c8d508e1e",
        #             "operator": "0bafc522-8011-43ba-978a-babe222ba466",
        #             "rules": [],
        #             "type": "string",
        #             "value": [
        #                 "\\N"
        #             ]
        #         }
        #     ],
        #     "type": null,
        #     "value": null
        # },

        # must be:
        rule_json = \
            {
                "condition": "AND",
                "rules": [
                    {
                        "id": "tagname",
                        "field": "tags.name",
                        "type": "string",
                        "input": "text",
                        "operator": "not_contains",
                        "value": "production"
                    },
                    {
                        "id": "tagname",
                        "field": "tags.name",
                        "type": "string",
                        "input": "text",
                        "operator": "begins_with",
                        "value": "development"
                    },
                    {
                        "condition": "OR",
                        "rules": [
                            {
                                "id": "type",
                                "field": "type",
                                "type": "string",
                                "input": "text",
                                "operator": "equal",
                                "value": "ec2"
                            },
                            {
                                "id": "type",
                                "field": "type",
                                "type": "string",
                                "input": "text",
                                "operator": "equal",
                                "value": "ami"
                            }
                        ]
                    }
                ]
            }

        evaluator = Evaluator(rule_json)
        object_1 = {'type': "ec2", "tags": [
            {"name": "hello"}, {"name": "asdfasfproduction_instance"}]}
        object_2 = {'type': "ami", "tags": [{"name": "development"}, {
            "name": "asfdafdroduction_instance"}, {"name": "proction"}]}
        objects = [object_1, object_2]

        # Assert
        assert rule['id'] == rule_id
        assert evaluator.get_matching_objects(objects) == [object_2]
