# rentry

<a href="https://rentry.co/"><img width="110" height="110" src="https://rentry.co/static/logo-border-fit.png" align="right" alt="rentry.co markdown paste repository"></a>

[Rentry.co](https://rentry.co) is a markdown-powered paste/publishing service with preview, custom urls and editing.

This repository contains the official Python clients for the rentry API:

- **`rentry.py`** — a self-contained command-line tool (single file, no dependencies)
- **`rentry_client`** — an installable Python library
- **`examples/`** — one runnable script per API use case
- an [API reference](#usage-api) for writing your own client

## Installation

```sh
pip install rentry
```

This installs both the `rentry` command-line tool and the `rentry_client` Python library. No dependencies.

### Single-file CLI (no pip)

The CLI also works as a single self-contained file:

```sh
wget https://raw.githubusercontent.com/radude/rentry/master/rentry.py -O ./rentry && chmod +x ./rentry
```

### From source

```sh
git clone https://github.com/radude/rentry.git
cd rentry
pip install .
```

To run the scripts in `examples/` you also need `pip install -r requirements.txt` (python-dotenv, for reading a `.env` file).

### Configuration

Both the CLI and the examples default to `https://rentry.co`. To target another instance (e.g. a local dev server), copy `env_example` to `.env` and adjust `BASE_PROTOCOL` / `BASE_URL`.

## Usage (Command-line)

```console
$ rentry --help

Usage: rentry {new | edit | raw | fetch | delete | update} {-h | --help} {-u | --url} {-p | --edit-code} {-f | --field} {-v | --value} {-a | --auth-code} text

Commands:
  new     create a new entry
  edit    edit an existing entry's text
  raw     get raw markdown text of an existing entry
  fetch   fetch an entry's full details (text, metadata, dates) as JSON
  delete  delete an entry
  update  update an entry's edit code, url or modify code

Options:
  -h, --help                 show this help message and exit
  -u, --url URL              url for the entry, random if not specified
  -p, --edit-code EDIT-CODE  edit code for the entry, random if not specified
  -f, --field FIELD-NAME     the field you wish to update (use on update command only)
  -v, --value VALUE          the value you wish to update (use on update command only)
  -a, --auth-code CODE       rentry-auth access code (use on raw command only)

Fields: (for use on update command only)
  edit_code
  url
  modify_code

Examples:
  rentry new 'markdown text'               # new entry with random url and edit code
  rentry new -p pw -u example 'text'       # with custom edit code and url
  rentry edit -p pw -u example 'text'      # edit the example entry
  cat FILE | rentry new                    # read from FILE and paste it to rentry
  cat FILE | rentry edit -p pw -u example  # read from FILE and edit the example entry
  rentry raw -u example                    # get raw markdown text
  rentry raw -u example -a CODE            # with a rentry-auth access code
  rentry raw -u https://rentry.co/example  # -u accepts absolute and relative urls
  rentry fetch -u example -p pw            # fetch full details as JSON

  rentry delete -p pw -u example          # deletes an entry
  rentry update -p pw -u example -f 'edit_code' -v 'new-pw'   # Sets the edit code to something new
  rentry update -p pw -u example -f 'url' -v 'new_url'        # Sets the url to something new
  rentry update -p pw -u example -f 'modify_code' -v 'm:1'    # Sets the modify code to something new
  rentry update -p pw -u example -f 'modify_code' -v ''       # Unsets the modify code
```

##### Url

Optional Url can be set (`-u, --url URL`)
It goes rentry.co/HERE. If no Url was set then random Url will be generated automatically.

##### Edit code

Optional edit code can be set (`-p, --edit-code EDIT-CODE`)
It can be used to edit the entry later. If no edit code was set then random edit code will be generated automatically. Generated edit code will be shown to you only once, so remember it or save it. You can share this code with anyone so a group of people can edit the same entry.

## Usage (Library)

```python
from rentry_client import RentryClient

client = RentryClient()  # or RentryClient('https://my-instance.example')

page = client.new(text='hello world', metadata={'PAGE_TITLE': 'Hello'})
print(page['url'], page['edit_code'])

client.edit(page['url_short'], page['edit_code'], text='updated!')

details = client.fetch(page['url_short'], page['edit_code'])
print(details)
```

Every method returns the parsed API response as a dict; `response['status']` is `'200'` on success, and errors are described in `response['content']` / `response['errors']`.

### Examples

Each script in [`examples/`](examples/) demonstrates exactly one use case and is runnable as-is:

| Script | Use case |
|---|---|
| [`examples/new.py`](examples/new.py) | Create a page, with metadata |
| [`examples/edit.py`](examples/edit.py) | Update a page's text with its edit code |
| [`examples/edit_upsert.py`](examples/edit_upsert.py) | Change some metadata options without replacing the rest |
| [`examples/edit_modify_code.py`](examples/edit_modify_code.py) | Set a modify code, then edit with it |
| [`examples/edit_secret_metadata.py`](examples/edit_secret_metadata.py) | SECRET_* metadata: preserved by default, opt in to change it |
| [`examples/edit_change_url.py`](examples/edit_change_url.py) | Move a page to a new url and rotate its edit code |
| [`examples/fetch.py`](examples/fetch.py) | Fetch a page's full details |
| [`examples/delete.py`](examples/delete.py) | Delete a page |
| [`examples/raw.py`](examples/raw.py) | Read raw text with a rentry-auth access code |

## Usage (API)

Send a standard POST request to the below endpoints. The /api endpoints are CSRF-exempt — no csrf token, cookies or Referer header are needed.

Starred fields are required. replace [url] with the actual URL in question (without brackets).

Example endpoint (Editing rentry.co/example): /edit/example

All fields that can be used as well as set (url, edit_code, modify_code) have new_ appended to their names when setting them.

### Metadata format

The metadata field accepts either of two syntaxes:

* Newline-separated `KEY = value` pairs, as on the website: `"PAGE_TITLE = Hello\nCONTAINER_MAX_WIDTH = 600px"`
* A JSON object: `{"OPTION_DISABLE_VIEWS": true, "CONTENT_TEXT_COLOR": ["grey", "red"]}`

The full list of metadata options (page, sharing, safety, container and content styling, secrets — ~63 in total) is documented at [rentry.co/metadata-how](https://rentry.co/metadata-how).

### Returns

* status
* content (if status is not 200, the error will be displayed here. Otherwise, all return values below are returned contained within this field)
* errors (on validation failures: the field-level error messages)

Responses are always delivered with HTTP 200; check the `status` value inside the JSON body. Statuses a client should handle: `200` success, `400` validation failed (details in `errors`), `403` access denied (raw access codes), `404` entry does not exist, `405` wrong HTTP method, `429` rate limited (back off and retry later), `503` database temporarily unavailable.

### /new

Fields:

* text *
* metadata
* url
* edit_code

Anonymous creation is rate-limited per IP (roughly 10 per minute on rentry.co; instance-configurable). A `429` status means slow down and retry later.

### /edit/[url]

You may provide a modify code to the edit_code field if one is set. Use this to give other people edit access to a page without the ability to steal it.

Fields:

* edit_code *
* text
* metadata
* update_mode
* update_secret_metadata ('true' or 'false', defaults to 'false' — see below)
* new_url
* new_edit_code
* new_modify_code (provide 'm:' to unset, this matches the website's functionality)

##### update_mode

* **replace** (the default): the edit replaces the page — text and the whole metadata set. Omitting text blanks the page, and metadata options omitted from the request are removed (except SECRET_* options, see update_secret_metadata below). For partial edits (e.g. only rotating a code), use upsert.
* **upsert**: the edit only changes what it provides. Metadata options in the request are added/updated, options omitted are kept, and an option sent with an empty value (`OPTION = `) is removed. Text is kept when omitted.

##### update_secret_metadata

SECRET_* metadata (SECRET_EMAIL_ADDRESS, SECRET_RAW_ACCESS_CODE, SECRET_VERIFY) is protected against accidental removal. When update_secret_metadata is 'false' or omitted, any SECRET_* option that was previously set on the entry is preserved as-is, no matter what the request sends for it — omitted, blanked, or changed values are all ignored for those keys.

To modify or remove a previously-set SECRET_* option, pass update_secret_metadata as the string 'true'. Adding a brand-new SECRET_* option to an entry that didn't have it never requires the flag. Alternatively, update_mode 'upsert' leaves omitted SECRETs untouched as before.

**Behavior change note:** clients that previously removed SECRET_* options by omitting them in a full-replace edit will now silently keep them until they add update_secret_metadata 'true'.

### /raw/[url]

Accepts GET or POST. Raw access is never open by default. Access codes are issued by rentry admins (contact support@rentry.co) — a page's SECRET_RAW_ACCESS_CODE metadata can only be set to an already-issued code (anything else is rejected at edit time). Raw access is granted when either:

* The request bears an issued access code in the **rentry-auth header** — this grants raw access to **all** pages.
* The page itself has an issued **SECRET_RAW_ACCESS_CODE** set — the page is then raw-readable by anyone, no header needed.

Denials return status `403` with a message explaining which condition failed.

Returns:

* text

To fetch metadata, please use /fetch endpoint

### /fetch/[url]

Fields:

* edit_code * (a modify code is also accepted here)

Returns:

* url
* url_case (if you set the URL with a different case structure than all lowercase, this will reflect that)
* views
* pub_date (YYYY-MM-DD T HH:MM:SS) (will not change if deleted and re-created)
* activated_date (if deleted and re-created, this is when this occured last)
* edit_date
* modify_code_set (bool)
* text
* metadata (returns as an object with key/value pairs. Each value is the entire set metadata value as a single string)
* metadata_version

### /delete/[url]

Fields:

* edit_code * (the full edit code only — a modify code cannot delete)
