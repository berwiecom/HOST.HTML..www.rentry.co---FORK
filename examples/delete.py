#!/usr/bin/env python3
"""Delete a page using its edit code."""

import os
from dotenv import load_dotenv
from rentry_client import RentryClient

load_dotenv()
base_url = os.getenv('BASE_PROTOCOL', 'https://') + os.getenv('BASE_URL', 'rentry.co')
client = RentryClient(base_url)

page = client.new(text='delete example')
assert page['status'] == '200', page['content']
print(page)

result = client.delete(page['url_short'], page['edit_code'])
print(result)
