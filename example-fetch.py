#!/usr/bin/env python3

import urllib.parse
import urllib.request
from json import loads as json_loads
from dotenv import load_dotenv, dotenv_values

load_dotenv()
env = dotenv_values()

# The /api endpoints are CSRF-exempt: no csrf token, cookies or Referer header needed.

class UrllibClient:
    """Simple HTTP client."""

    def get(self, url, headers={}):
        request = urllib.request.Request(url, headers=headers)
        return self._request(request)

    def post(self, url, data=None, headers={}):
        postdata = urllib.parse.urlencode(data).encode()
        request = urllib.request.Request(url, postdata, headers)
        return self._request(request)

    def _request(self, request):
        response = urllib.request.urlopen(request)
        response.status_code = response.getcode()
        response.data = response.read().decode('utf-8')
        return response

client = UrllibClient()

## First, create
payload = {
    'text': 'test',
    'metadata' : 'OPTION_DISABLE_VIEWS = true',
}
result_create = json_loads(client.post(f"{env['BASE_PROTOCOL']}{env['BASE_URL']}" + '/api/new', payload).data)
print(result_create)

## Then, fetch
payload = {
    'edit_code' : result_create['edit_code'],
}
result_fetch = client.post(f"{env['BASE_PROTOCOL']}{env['BASE_URL']}" + f"/api/fetch/{result_create['url_short']}", payload).data
print(result_fetch)
