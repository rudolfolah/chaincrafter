# Documentation for chaincrafter

## Install

```bash
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
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