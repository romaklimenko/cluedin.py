import requests

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

def rule_json_to_querybuilder():
  pass

def rule_operator_id_to_querybuilder_string(rule_operator_id):
  match rule_operator_id:
    case '0bafc522-8011-43ba-978a-babe222ba466':
      return 'equal'
    # TODO: add more cases
    case _:
      return None
