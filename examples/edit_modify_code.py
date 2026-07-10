#!/usr/bin/env python3
"""Set a modify code, then edit with it.

A modify code ('m:...') lets other people edit a page without being able to
steal it: it cannot change the edit code, url, modify code or SECRET options,
and cannot delete the page.
"""

import os
from dotenv import load_dotenv
from rentry_client import RentryClient

load_dotenv()
base_url = os.getenv('BASE_PROTOCOL', 'https://') + os.getenv('BASE_URL', 'rentry.co')
client = RentryClient(base_url)

page = client.new(text='modify code example')
assert page['status'] == '200', page['content']
print(page)

# Set a modify code using the edit code. (Pass new_modify_code='m:' to unset one.)
result = client.edit(page['url_short'], page['edit_code'], new_modify_code='m:example-code')
print(result)

# Edit using the modify code in place of the edit code.
result = client.edit(page['url_short'], 'm:example-code', text='edited via modify code')
print(result)
