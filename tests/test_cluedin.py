import os
from cluedin import cluedin

from jqqb_evaluator.evaluator import Evaluator

from json import dumps

from dotenv import load_dotenv
load_dotenv()


class TestCluedIn:
  def xtest_get_a_token(self):
    # Arrange
    username = os.environ.get('USER')
    password = os.environ.get('PASSWORD')
    org_name = os.environ.get('ORGANIZATION')
    auth_url = os.environ.get('AUTH_URL')
    # Act
    token = cluedin.get_token(username, password, org_name, auth_url)
    # Assert
    assert len(token) > 2000

  def xtest_search(self):
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
    assert cluedin.rule_operator_id_to_querybuilder_string('0bafc522-8011-43ba-978a-babe222ba466') == 'equal'

  def test_rule_json_to_querybuilder(self):
    # Arrange
    property_map = {
      'Properties[IMDb.name.basic.BirthYear]': 'birthYear',
      'Properties[IMDb.name.basic.DeathYear]': 'deathYear',
    }

    rule_json = {
      'id': 'fc41d4ea-95a5-4d2e-8e8e-4b14a7e93c2e',
      'name': 'Complex Rule',
      'description': "[{\"type\":\"paragraph\",\"children\":[{\"text\":\"Tag entities with invalid dates.\"}]}]",
      'organizationId': '0130ffc7-e435-4a28-8d57-7f236c339277',
      'type': 'ProcessingRule',
      'order': 2,
      'createdBy': 'cd42615b-5552-4244-a97f-a9ae4f214133',
      'createdAt': '2022-02-16T15:52:02.7396045+00:00',
      'modifiedBy': 'cd42615b-5552-4244-a97f-a9ae4f214133',
      'modifiedAt': '2022-02-16T16:01:40.7123697+00:00',
      'isActive': True,
      'ownedBy': 'cd42615b-5552-4244-a97f-a9ae4f214133',
      'conditions': {
        'objectTypeId': '00000000-0000-0000-0000-000000000000',
        'condition': 'AND',
        'field': None,
        'id': 'd7f7a043-f136-4a12-b0ab-5c8eeb87acea',
        'operator': '00000000-0000-0000-0000-000000000000',
        'rules': [
          {
            'objectTypeId': '00000000-0000-0000-0000-000000000000',
            'condition': 'AND',
            'field': None,
            'id': 'fe5a0ff9-c7ea-4194-bd8b-4b9f87723bf8',
            'operator': '00000000-0000-0000-0000-000000000000',
            'rules': [
              {
                'objectTypeId': '3be85371-cbe0-4180-8820-73e6e37a6c32',
                'condition': 'AND',
                'field': 'EntityType',
                'id': '4118f2e7-8b85-4386-9b12-080a9f97717f',
                'operator': '0bafc522-8011-43ba-978a-babe222ba466',
                'rules': [],
                'type': 'string',
                'value': [
                  '/Infrastructure/User'
                ]
              }
            ],
            'type': 'rule',
            'value': None
          },
          {
            'objectTypeId': '00000000-0000-0000-0000-000000000000',
            'condition': 'OR',
            'field': None,
            'id': '2915d458-d374-491b-b2e4-baa8e55b16c0',
            'operator': '00000000-0000-0000-0000-000000000000',
            'rules': [
              {
                  'objectTypeId': '011ac3b4-0b46-4f9c-a82a-8c14f9dd642b',
                  'condition': 'AND',
                  'field': 'Properties[IMDb.name.basic.BirthYear]',
                  'id': '01323e3e-77c1-43ed-9151-3f7a1975e872',
                  'operator': '0bafc522-8011-43ba-978a-babe222ba466',
                  'rules': [],
                  'type': 'string',
                  'value': [
                    '\\N'
                  ]
              },
              {
                'objectTypeId': '011ac3b4-0b46-4f9c-a82a-8c14f9dd642b',
                'condition': 'AND',
                'field': 'Properties[IMDb.name.basic.DeathYear]',
                'id': 'b34ce52c-9201-4054-8314-a2ceaf2a0cc2',
                'operator': '0bafc522-8011-43ba-978a-babe222ba466',
                'rules': [],
                'type': 'string',
                'value': [
                  '\\N'
                ]
              }
            ],
            'type': 'rule',
            'value': None
          }
        ],
        'type': None,
        'value': None
      },
      'actions': [
        {
          'name': 'Add Tag',
          'supportsPreview': False,
          'properties': [
            {
              'name': 'Value',
              'type': 'System.String',
              'friendlyType': None,
              'friendlyName': None,
              'value': 'invalid-date'
            }
          ],
          'type': 'CluedIn.Rules.Actions.AddTag, CluedIn.Rules, Version=3.2.0.0, Culture=neutral, PublicKeyToken=null'
        }
      ]
    }

    expected_querybuilder_json = {
      'condition': 'AND',
      'id': 'd7f7a043-f136-4a12-b0ab-5c8eeb87acea',
      'rules': [
        {
          'condition': 'AND',
          'id': 'fe5a0ff9-c7ea-4194-bd8b-4b9f87723bf8',
          'rules': [
            {
              'condition': 'AND',
              'field': 'EntityType',
              'id': '4118f2e7-8b85-4386-9b12-080a9f97717f',
              'operator': 'equal',
              'rules': [],
              'type': 'string',
              'value': '/Infrastructure/User'
            }
          ],
          'type': 'rule',
        },
        {
          'condition': 'OR',
          'id': '2915d458-d374-491b-b2e4-baa8e55b16c0',
          'rules': [
            {
              'condition': 'AND',
              'field': 'birthYear',
              'id': '01323e3e-77c1-43ed-9151-3f7a1975e872',
              'operator': 'equal',
              'rules': [],
              'type': 'string',
              'value': '\\N'
            },
            {
              'condition': 'AND',
              'field': 'deathYear',
              'id': 'b34ce52c-9201-4054-8314-a2ceaf2a0cc2',
              'operator': 'equal',
              'rules': [],
              'type': 'string',
              'value': '\\N'
            }
          ],
          'type': 'rule',
        }
      ]
    }
    # Act
    result = cluedin.rule_json_to_querybuilder(rule_json['conditions'], property_map)
    # Assert
    assert dumps(result) == dumps(expected_querybuilder_json)

    evaluator = Evaluator(result)

    shall_pass_one = {
      'EntityType': '/Infrastructure/User',
      'birthYear': '\\N',
      'deathYear': '2001'
    }

    shall_pass_two = {
      'EntityType': '/Infrastructure/User',
      'birthYear': '1981',
      'deathYear': '\\N'
    }

    shall_not_pass = {
      'EntityType': '/Infrastructure/Organization',
      'birthYear': '1809',
      'deathYear': '1865'
    }

    objects = [shall_pass_one, shall_pass_two, shall_not_pass]
    assert evaluator.get_matching_objects(objects) == [shall_pass_one, shall_pass_two]

  def xtest_run_rules(self):
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

    # must be:
    rule_json = {
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
