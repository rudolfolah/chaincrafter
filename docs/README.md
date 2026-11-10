# Documentation for chaincrafter

## Install

Use Python 3.15.2 for the latest documentation dependencies (Python 3.9+ is
required for the documentation toolchain, independently of the library's
Python 3.8+ support).


```bash
python3.15 -m venv ./venv
source ./venv/bin/activate
python -m pip install --upgrade -r requirements.txt
```

## Build and Serve Locally

```bash
cd docs/
mkdocs build # static build
mkdocs serve # live-reloading server
```

## Deploying

* [Deploying to GitHub Pages](https://www.mkdocs.org/user-guide/deploying-your-docs/#github-pages)
* [Deploying to Read The Docs](https://www.mkdocs.org/user-guide/deploying-your-docs/#read-the-docs)

GitHub Pages deploy will create the `gh-pages` branch and push the documentation there

```bash
cd docs/
mkdocs gh-deploy
```