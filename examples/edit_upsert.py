#!/usr/bin/env python3
"""Change some metadata options without replacing the rest, using update_mode='upsert'."""

import os
from dotenv import load_dotenv
from rentry_client import RentryClient

load_dotenv()
base_url = os.getenv('BASE_PROTOCOL', 'https://') + os.getenv('BASE_URL', 'rentry.co')
client = RentryClient(base_url)

page = client.new(
    text='upsert example',
    metadata={'OPTION_DISABLE_VIEWS': True, 'CONTAINER_MAX_WIDTH': '600px'},
)
assert page['status'] == '200', page['content']
print(page)

# Only CONTAINER_PADDING is added/updated; the options set above are kept.
# Text is also kept when not provided. In the default (replace) mode, this
# call would have replaced the whole metadata set instead.
result = client.edit(
    page['url_short'],
    page['edit_code'],
    update_mode='upsert',
    metadata={'CONTAINER_PADDING': '10px'},
)
print(result)

# Remove an existing option in upsert mode by sending it with a blank value.
# Here CONTAINER_MAX_WIDTH is removed while everything else is kept. (In the
# default replace mode you would instead just omit the key. A blank value in
# replace mode is an error, not a removal.) SECRET_* options need the extra
# update_secret_metadata=True flag to be removed this way.
result = client.edit(
    page['url_short'],
    page['edit_code'],
    update_mode='upsert',
    metadata={'CONTAINER_MAX_WIDTH': ''},
)
print(result)
