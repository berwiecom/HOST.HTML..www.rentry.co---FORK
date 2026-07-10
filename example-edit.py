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
    'metadata' : 'SECRET_EMAIL_ADDRESS = support@rentry.co',
}
result_create = json_loads(client.post(f"{env['BASE_PROTOCOL']}{env['BASE_URL']}" + '/api/new', payload).data)
print(result_create)

## Then, edit
payload = {
    'text': 'test updated!',
    'edit_code' : result_create['edit_code'],
    'new_modify_code' : 'm:abc',
    'update_mode' : 'upsert', # This causes only these metadata options to change, rather than a full replacement. Remove if you want to replace fully.
    'metadata' : 'CONTAINER_PADDING = 10px \n \
CONTAINER_MAX_WIDTH = 600px  \n \
CONTAINER_INNER_FOREGROUND_COLOR = RGBA(123,123,123,0.2) \n \
CONTAINER_INNER_BACKGROUND_COLOR = transparent \n \
CONTAINER_INNER_BACKGROUND_IMAGE = https://rentry.co/static/icons/512.png'
}
result_edit = client.post(f"{env['BASE_PROTOCOL']}{env['BASE_URL']}" + f"/api/edit/{result_create['url_short']}", payload).data
print(result_edit)

## Edit Using modify code
payload = {
    'text': 'test updated using modify',
    'edit_code' : 'm:abc',
    'update_mode' : 'upsert',
    'metadata' : "CONTENT_FONT_WEIGHT = 600 \n \
    "
}
result_edit = client.post(f"{env['BASE_PROTOCOL']}{env['BASE_URL']}" + f"/api/edit/{result_create['url_short']}", payload).data
print(result_edit)

## Replace mode + safe default: SECRETs auto-preserved.
# Without update_secret_metadata, the previously-set SECRET_EMAIL_ADDRESS is kept
# even though the metadata payload omits it.
payload = {
    'text': 'test updated (default preserves SECRETs)',
    'edit_code' : result_create['edit_code'],
    'metadata' : 'PAGE_TITLE = Test',
    # update_secret_metadata not set -> defaults to 'false' -> SECRETs preserved
}
result_edit = client.post(f"{env['BASE_PROTOCOL']}{env['BASE_URL']}" + f"/api/edit/{result_create['url_short']}", payload).data
print(result_edit)

## Replace mode + explicit opt-in: modify or remove a SECRET.
# update_secret_metadata 'true' is REQUIRED to modify or remove previously-set
# SECRET_* fields in replace mode. (Adding a brand-new SECRET does not need it.)
# Pass the string 'true' or 'false' only. This guards against accidental loss of
# the recovery email / raw access code.
payload = {
    'text': 'test updated (explicit SECRET change)',
    'edit_code' : result_create['edit_code'],
    'metadata' : 'SECRET_EMAIL_ADDRESS = new@example.com',
    'update_secret_metadata' : 'true',
}
result_edit = client.post(f"{env['BASE_PROTOCOL']}{env['BASE_URL']}" + f"/api/edit/{result_create['url_short']}", payload).data
print(result_edit)