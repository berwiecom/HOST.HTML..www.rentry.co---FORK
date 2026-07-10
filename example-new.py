#!/usr/bin/env python3

import urllib.parse
import urllib.request
import json
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

# Provide metadata as a newline separated string, as on the website
metadata = 'OPTION_DISABLE_VIEWS = true \n \
    CONTAINER_MAX_WIDTH = 600px '

# Or, Format metadata as JSON
metadata_obj = {
    'OPTION_DISABLE_VIEWS' : True,
    'CONTENT_TEXT_COLOR' : ['grey', 'red'],
}
metadata = json.dumps(metadata_obj)


payload = {
    'text': 'test',
    'metadata' : metadata
}
result = json.loads(client.post(f"{env['BASE_PROTOCOL']}{env['BASE_URL']}" + '/api/new', payload).data)
print(result)
