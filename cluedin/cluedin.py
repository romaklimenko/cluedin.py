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

