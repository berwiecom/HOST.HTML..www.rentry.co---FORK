# Releasing to PyPI

The package publishes to <https://pypi.org/project/rentry/> — owned by the
`radude` PyPI account (admin@rentry.co). Last pre-automation release was 1.0.1
(2018); 2.0.0 onward come from this repo.

## One-time setup

1. **Account access.** Log in at pypi.org as `radude`. If the password is
   lost, reset via admin@rentry.co. PyPI requires 2FA on all publishing
   accounts — you'll be prompted to enrol (authenticator app or passkey) on
   first login. Store the recovery codes.
2. **Trusted publishing (recommended, no tokens).** On the PyPI project page:
   *Manage → Publishing → Add a new publisher* with:
   - Owner: `radude`, Repository: `rentry`
   - Workflow name: `publish.yml`
   - Environment: `pypi`
   Then on GitHub: repo *Settings → Environments → New environment* named
   `pypi` (optionally add required reviewers to gate releases).
3. **Fallback (manual uploads).** Instead of (2): PyPI *Account settings →
   API tokens → Add token* scoped to the `rentry` project. Uploads use
   username `__token__` and the token as password — plain username/password
   uploads are no longer accepted.

## Releasing a version

1. Bump the version in **both** `pyproject.toml` and
   `src/rentry_client/__init__.py`.
2. Sanity-check locally:
   ```sh
   python -m build
   python -m twine check dist/*
   pip install --force-reinstall dist/rentry-<version>-py3-none-any.whl
   rentry --help
   ```
3. Commit, tag `v<version>`, push, and create a GitHub release for the tag.
   The `publish.yml` workflow builds and uploads to PyPI.

Manual alternative (fallback token from one-time setup step 3):

```sh
python -m build
python -m twine upload dist/*
```

## Rules of the index

- A version, once uploaded, is **permanent** — it can be yanked but never
  replaced. Any fix means a new version number.
- Versions must be strictly increasing (2.0.0 supersedes 1.0.1).
- To rehearse, upload to <https://test.pypi.org> first (separate account and
  token): `twine upload --repository testpypi dist/*`.

## Compatibility contract (2.0.0)

`pip install rentry` must keep providing a `rentry` command whose 1.0.1-era
interface is unchanged: `new`/`edit`/`raw` commands, `-h/-u/-p` flags, stdin
piping, same output format and exit codes, defaulting to https://rentry.co
with zero configuration and zero required dependencies. New commands/flags and
the `rentry_client` library are strict additions.
