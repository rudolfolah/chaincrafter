# Build and Publish, chaincrafter - Python

Use Python 3.15.2 for release tooling. The published library continues to support
Python 3.8+; build-time dependencies are selected separately for each interpreter.

* Update the version, dependencies, and [classifiers](https://pypi.org/classifiers/) in `pyproject.toml`, the single source of package metadata.
* Check the Python 3.8–3.15 CI matrix before publishing.
* Create separate API tokens on [TestPyPI](https://test.pypi.org/manage/account/) and [PyPI](https://pypi.org/manage/account/); a token only works on the site where it was created.
* At each upload prompt, enter `__token__` as the username and that site's token (including the `pypi-` prefix) as the password.
  TestPyPI and PyPI use separate tokens. For non-interactive uploads, configure the appropriate credentials in `~/.pypirc`.

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
