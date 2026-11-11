# Local Development, chaincrafter - Python

Run these commands from `python/`. The repository's `.python-version` selects
Python 3.15.2 for development; the library supports Python 3.8 through 3.15.

```bash
uv python install
uv venv --seed venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[openai]'
python -m unittest discover -s tests -v
```

Without uv, install Python 3.15.2 and use `python3.15 -m venv venv` instead.
For core-only development, omit `[openai]`; `requirements.txt` also installs the
core package using the dependencies declared in `pyproject.toml`.

## Python compatibility

Dependency minimums follow the newest compatible releases at the time of this
upgrade. Installers may select newer compatible releases automatically.

| Python | pandas minimum | OpenAI SDK minimum (optional) |
| --- | --- | --- |
| 3.8 | 2.0.3 | 2.2.0 (below 2.3) |
| 3.9 | 2.3.3 | 2.48.0 |
| 3.10 | 2.3.3 | 3.48.0 |
| 3.11–3.15 | 3.1.1 | 3.48.0 |

PyYAML requires at least 6.0.3 on every supported Python version. Python 3.8
also constrains NumPy below 2 to keep pandas 2.0 binary-compatible. Build
isolation selects a compatible setuptools release for each interpreter.
The Python 3.8 OpenAI SDK stays below 2.3 because later releases require a
`jiter` version that only supports Python 3.9+, despite some SDK releases
declaring Python 3.8 support.
Python 3.8–3.10 are end-of-life upstream; compatibility does not provide upstream
security fixes. Prefer Python 3.15.2 for new environments.

CI builds source distributions and wheels on every Python minor from 3.8 to
3.15, then tests the installed wheel outside the source tree. OpenAI regression
tests use the installed SDK against a local HTTP server, without API credentials
or external API requests. The test clears inherited SDK and proxy environment
settings so requests stay local.

## Testing in another package

```bash
python -m pip install --upgrade build
python -m build
# Install the wheel in another project's environment.
python -m pip install /path/to/chaincrafter/python/dist/chaincrafter-0.2.4-py3-none-any.whl
```

Model-specific imports should remain inside `__init__` or `complete` so optional
integrations are not required to import the core library.
