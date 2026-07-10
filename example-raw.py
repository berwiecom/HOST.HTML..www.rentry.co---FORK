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

# This example does not work without further adjustments!
# To use the /raw endpoint you must have a SECRET_RAW_ACCESS_CODE. You can request one from support@rentry.co.
# Either set this value in each of your page, or use it below as a custom header.

example_url = '10'

_headers = {'rentry-auth': ''}

result_raw = json_loads(client.post(f"{env['BASE_PROTOCOL']}{env['BASE_URL']}" + f'/api/raw/{example_url}', {}, headers=_headers).data)
print(result_raw)
