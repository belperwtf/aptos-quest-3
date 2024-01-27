import requests

class GraphQLClient:
    def __init__(self, url):
        self.url = f"{url}/graphql"

    def execute_query(self, query, variables=None, headers=None):
        headers = headers or {}
        payload = {
            'query': query,
            'variables': variables
        }

        response = requests.post(self.url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Query failed with status code {response.status_code}: {response.text}")
