# Python client for CluedIn API

```python
from cluedin import cluedin

def test_search(self):
  # Arrange
  username = os.environ.get('USERNAME')
  password = os.environ.get('PASSWORD')
  org_name = os.environ.get('ORG_NAME')
  auth_url = os.environ.get('AUTH_URL')
  api_url = os.environ.get('API_URL')
  token = cluedin.get_token(username, password, org_name, auth_url)
  # Act
  result = cluedin.search(token, api_url, "*", ['id', 'name'])
  # Assert
  assert len(result['data']['search']['entries']) == 20
```