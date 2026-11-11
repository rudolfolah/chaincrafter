# Build and Publish, chaincrafter - Python

Use Python 3.15.2 for release tooling. The published library continues to support
Python 3.8+; build-time dependencies are selected separately for each interpreter.

* Update the version, dependencies, and [classifiers](https://pypi.org/classifiers/) in `pyproject.toml`, the single source of package metadata.
* Check the Python 3.8–3.15 CI matrix before publishing.
* [Create an API token](https://pypi.org/manage/account/).
  * Set your username to `__token__`.
  * Set your password to the token value, including the `pypi-` prefix.

```bash
cd /path/to/chaincrafter/python
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*

# Test upload (use the artifacts for the version being released).
python -m twine upload -r testpypi dist/chaincrafter-0.2.4*

# Upload.
python -m twine upload dist/chaincrafter-0.2.4*
```
