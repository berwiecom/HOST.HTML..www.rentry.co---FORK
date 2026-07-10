#!/usr/bin/env python3
"""Get a page's raw markdown text via the /api/raw endpoint.

This example does not work without further adjustments! Raw access is never
open by default. Access codes are issued by rentry admins (request one from
support@rentry.co); a page's SECRET_RAW_ACCESS_CODE metadata can only be set
to an already-issued code. Access is granted when either:
- the request bears an issued access code (passed as auth_code below) — this
  grants raw access to ALL pages, or
- the page itself has an issued SECRET_RAW_ACCESS_CODE set — the page is then
  raw-readable without any auth_code.
"""

import os
from dotenv import load_dotenv
from rentry_client import RentryClient

load_dotenv()
base_url = os.getenv('BASE_PROTOCOL', 'https://') + os.getenv('BASE_URL', 'rentry.co')
client = RentryClient(base_url)

result = client.raw('example-url', auth_code='')
print(result)
