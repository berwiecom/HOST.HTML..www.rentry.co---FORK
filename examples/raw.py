#!/usr/bin/env python3
"""Get a page's raw markdown text via the /api/raw endpoint.

Raw access is never open by default. Access codes are issued by rentry admins
(request one from support@rentry.co); a page's SECRET_RAW_ACCESS_CODE metadata
can only be set to an already-issued code. Access is granted when either:
- the request bears an issued access code (passed as auth_code below)
  or
- the page itself has an issued SECRET_RAW_ACCESS_CODE set.

This example creates a page and then reads it back over raw using an issued
access code from the RAW_ACCESS_CODE environment variable.
"""

import os
from dotenv import load_dotenv
from rentry_client import RentryClient

load_dotenv()
base_url = os.getenv('BASE_PROTOCOL', 'https://') + os.getenv('BASE_URL', 'rentry.co')
auth_code = os.getenv('RAW_ACCESS_CODE', '')
client = RentryClient(base_url)

# Create a page to read back over raw.
page = client.new(text='raw access example')
assert page['status'] == '200', page['content']
print(page)

# An issued access code grants raw access to any page, including the one we
# just created. Without a valid auth_code the API returns an error explaining
# how to obtain one.
result = client.raw(page['url_short'], auth_code=auth_code)
print(result)
