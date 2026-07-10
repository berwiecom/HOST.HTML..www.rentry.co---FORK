#!/usr/bin/env python3
"""Get a page's raw markdown text via the /api/raw endpoint.

This example does not work without further adjustments! Access requires either:
- a rentry-auth access code (request one from support@rentry.co), passed as
  auth_code below — this grants access to all pages, or
- the page's own SECRET_RAW_ACCESS_CODE metadata value, passed the same way.
"""

import os
from dotenv import load_dotenv
from rentry_client import RentryClient

load_dotenv()
base_url = os.getenv('BASE_PROTOCOL', 'https://') + os.getenv('BASE_URL', 'rentry.co')
client = RentryClient(base_url)

result = client.raw('example-url', auth_code='')
print(result)
