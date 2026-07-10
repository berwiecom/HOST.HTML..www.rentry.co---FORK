#!/usr/bin/env python3
"""Create a new page."""

import os
from dotenv import load_dotenv
from rentry_client import RentryClient

load_dotenv()
base_url = os.getenv('BASE_PROTOCOL', 'https://') + os.getenv('BASE_URL', 'rentry.co')
client = RentryClient(base_url)

# metadata is a dict, sent to the API as JSON. A newline-separated string,
# as on the website, works too, e.g.:
#   metadata='OPTION_DISABLE_VIEWS = true \n CONTAINER_MAX_WIDTH = 600px'
result = client.new(
    text='hello world',
    metadata={'OPTION_DISABLE_VIEWS': True, 'CONTAINER_MAX_WIDTH': '600px'},
    # url='custom-url',            # random if not given
    # edit_code='custom-code',     # random if not given
)
print(result)
