#!/usr/bin/env python3
"""Fetch a page's full details (text, metadata, views, dates) using its edit code."""

import os
from dotenv import load_dotenv
from rentry_client import RentryClient

load_dotenv()
base_url = os.getenv('BASE_PROTOCOL', 'https://') + os.getenv('BASE_URL', 'rentry.co')
client = RentryClient(base_url)

page = client.new(text='fetch example', metadata={'OPTION_DISABLE_VIEWS': True})
assert page['status'] == '200', page['content']
print(page)

result = client.fetch(page['url_short'], page['edit_code'])
print(result)
