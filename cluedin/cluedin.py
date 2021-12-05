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

  data = f'{{ "query": "{{ search(query:\\"{query}\\") {{ entries {{ { ", ".join(entries) } }} }} }}" }}'

  response = requests.post(f'{api_url}/graphql', data=data, headers=headers)
  return response.json()
