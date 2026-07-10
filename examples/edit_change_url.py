#!/usr/bin/env python3
"""Move a page to a new url and rotate its edit code."""

import os
import secrets
from dotenv import load_dotenv
from rentry_client import RentryClient

load_dotenv()
base_url = os.getenv('BASE_PROTOCOL', 'https://') + os.getenv('BASE_URL', 'rentry.co')
client = RentryClient(base_url)

page = client.new(text='change url example')
assert page['status'] == '200', page['content']
print(page)

# Random suffixes so reruns don't collide with an existing url.
new_url = page['url_short'] + '-moved-' + secrets.token_hex(4)
new_edit_code = 'rotated-' + secrets.token_hex(4)

# upsert leaves the page's text and metadata untouched. Without it this would
# be a replace-mode edit, and omitting text in replace mode blanks the page.
result = client.edit(
    page['url_short'],
    page['edit_code'],
    update_mode='upsert',
    new_url=new_url,
    new_edit_code=new_edit_code,
)
print(result)

# The page now answers at the new url, with the new edit code only.
result = client.fetch(new_url, new_edit_code)
print(result)
