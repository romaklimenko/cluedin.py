import requests
from copy import deepcopy
from itertools import repeat

def get_token(username, password, org_name, auth_url):
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  data = {
    'username': username,
    'password': password,
    'client_id': org_name,
    'grant_type': 'password'
  }
  response = requests.post(auth_url, headers=headers, data=data)
  return response.json()['access_token']

def search(token, api_url, query, entries):
  headers = {
    'Authorization': 'Bearer {}'.format(token),
    'Content-Type': 'application/json'
  }

  args = {
    'query': query,
    'entries': ','.join(entries)
  }

  # data = f'{{ query: "{{ search(query:\\"{query}\\") {{ entries {{ { ", ".join(entries) } }}, cursor }} }}" }}'
  gql_query = """{{
    query: "{{
      search(query:\\"{query}\\") {{
        entries {{
          {entries}
        }},
        cursor
      }}
    }}"
  }}""".format(**args)

  response = requests.post(
    f'{api_url}/graphql',
    data=gql_query,
    headers=headers)

  return response.json()

def get_rule(token, api_url, rule_id):
  headers = {
    'Authorization': 'Bearer {}'.format(token),
    'Content-Type': 'application/json'
  }

  response = requests.get(
    f'{api_url}/rules/{rule_id}',
    headers=headers)

  return response.json()

def rule_json_to_querybuilder(rule_json, property_map):
  result = deepcopy(rule_json)
  result.pop('objectTypeId', None)
  for key in ['field', 'type', 'value']:
    if result[key] == None:
      result.pop(key, None)
  if result['operator'] == '00000000-0000-0000-0000-000000000000':
    result.pop('operator', None)
  else:
    result['operator'] = rule_operator_id_to_querybuilder_string(result['operator'])
  
  if 'value' in result and len(result['value']) == 1:
    result['value'] = result['value'][0]

  if 'field' in result and result['field'] in property_map:
    result['field'] = property_map[result['field']]

  result['rules'] = list(map(rule_json_to_querybuilder, result['rules'], repeat(property_map)))

  return result

def rule_operator_id_to_querybuilder_string(rule_operator_id):
  match rule_operator_id:
    case '0bafc522-8011-43ba-978a-babe222ba466':
      return 'equal'
    # TODO: add more cases
    case _:
      return None
