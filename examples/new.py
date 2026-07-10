#!/usr/bin/env python3
"""Create a new page."""

import os
from dotenv import load_dotenv
from rentry_client import RentryClient

load_dotenv()
base_url = os.getenv('BASE_PROTOCOL', 'https://') + os.getenv('BASE_URL', 'rentry.co')
client = RentryClient(base_url)

# metadata is a newline-separated string, as on the website.
# A dict works too and is sent as JSON, e.g.:
#   metadata={'OPTION_DISABLE_VIEWS': True, 'CONTENT_TEXT_COLOR': ['grey', 'red']}
result = client.new(
    text='hello world',
    metadata='OPTION_DISABLE_VIEWS = true \n CONTAINER_MAX_WIDTH = 600px',
    # url='custom-url',            # random if not given
    # edit_code='custom-code',     # random if not given
)
print(result)
