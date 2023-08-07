# chaincrafter - Python

## Local Development

```bash
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

To test different models, install the packages required, for example with OpenAI, run `pip install openai`.

The imports for the models should be part of the `__init__` or the `complete` method of the `ChatModel` class.

## Build and Publish

* [Update classifiers in `pyproject.toml` and `setup.py`](https://pypi.org/classifiers/)
* [Update project metadata](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#declaring-project-metadata)

```bash
cd /path/to/chaincrafter/python
pip install build
python -m build
```

### Testing in another package

```bash
python setup.py sdist
# install the package in another project
pip install /path/to/chaincrafter/python/dist/chaincrafter-0.1.0.tar.gz
```
