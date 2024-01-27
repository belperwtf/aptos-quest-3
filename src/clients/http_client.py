import requests

class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, path, params=None, headers=None):
        url = self.base_url + path
        response = requests.get(url, params=params, headers=headers)
        return response

    def post(self, path, data=None, json=None, headers=None):
        url = self.base_url + path
        response = requests.post(url, data=data, json=json, headers=headers)
        return response
