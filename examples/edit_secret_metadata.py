#!/usr/bin/env python3
"""Edit SECRET_* metadata, which is protected against accidental removal.

Previously-set SECRET_* options (SECRET_EMAIL_ADDRESS, SECRET_RAW_ACCESS_CODE,
SECRET_VERIFY) are preserved by default no matter what an edit sends — omitted,
blanked or changed values are all ignored for those keys. Pass
update_secret_metadata=True to allow an edit to change or remove them.
Adding a brand-new SECRET_* option never requires the flag.
"""

import os
from dotenv import load_dotenv
from rentry_client import RentryClient

load_dotenv()
base_url = os.getenv('BASE_PROTOCOL', 'https://') + os.getenv('BASE_URL', 'rentry.co')
client = RentryClient(base_url)

page = client.new(
    text='secret metadata example',
    metadata={'SECRET_EMAIL_ADDRESS': 'someone@example.com'},
)
assert page['status'] == '200', page['content']
print(page)

# Full-replace edit that omits the SECRET: it is preserved anyway, because
# update_secret_metadata defaults to false.
result = client.edit(
    page['url_short'],
    page['edit_code'],
    text='SECRET survives this edit',
    metadata={'PAGE_TITLE': 'Example'},
)
print(result)

# Trying to CHANGE the SECRET without the flag fails SILENTLY: the API returns
# status 200 as if it worked, but SECRET_EMAIL_ADDRESS keeps its old value.
# There is no error in the response.
result = client.edit(
    page['url_short'],
    page['edit_code'],
    text='this edit does not actually change the SECRET',
    metadata={'SECRET_EMAIL_ADDRESS': 'new@example.com'},
    #update_secret_metadata=True,
)
print(result)

# To actually change a previously-set SECRET, opt in explicitly.
result = client.edit(
    page['url_short'],
    page['edit_code'],
    text='SECRET changed by this edit',
    metadata={'SECRET_EMAIL_ADDRESS': 'new@example.com'},
    update_secret_metadata=True,
)
print(result)

# Removing a previously-set SECRET also needs the opt-in flag. In the default
# (replace) mode, drop the key by omitting it from the metadata. In upsert mode,
# send it blank instead — see edit_upsert.py for that pattern.
result = client.edit(
    page['url_short'],
    page['edit_code'],
    text='SECRET removed by this edit',
    metadata={'PAGE_TITLE': 'Example'},  # SECRET_EMAIL_ADDRESS omitted -> removed
    update_secret_metadata=True,
)
print(result)
