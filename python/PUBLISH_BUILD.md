# Build and Publish, chaincrafter - Python

* [Update classifiers in `pyproject.toml` and `setup.py`](https://pypi.org/classifiers/)
* [Update project metadata](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#declaring-project-metadata)
* [Create an API token](https://pypi.org/manage/account/)
  * Set your username to `__token__`
  * Set your password to the token value, including the `pypi-` prefix 

```bash
cd /path/to/chaincrafter/python
pip install build
python -m build

pip install twine
# test upload
twine upload -r testpypi dist/chaincrafter-0.2.1*

# upload
twine upload dist/chaincrafter-0.2.1*
```
