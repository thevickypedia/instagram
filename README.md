# Instagram
Python script to retrieve data from Instagram

## Usage
#### Env Variables:
```
export insta_user=<username>
export insta_pass=<password>
```
#### Setup:
`pip3 install -r requirements.txt`
#### Commit:
`pre-commit run --all-files` - This will ensure linting and generates docs from docstrings.

Page hosted at https://thevickypedia.github.io/instagram/

<!--
## Replicate auto generation of pages
`pip3 install sphinx`<br>
`cd doc_generator`<br>
`sphinx-quickstart`<br>
### Addition to index.rst
```
.. automodule:: instagram.ig_connector
   :members:
   :undoc-members:
```
### Modifications to conf.py
- Insert and append file path for entry point script and libraries.
```
import os
import sys
from pathlib import Path
sys.path.insert(0, os.path.abspath('../..'))
sys.path.append(f'{Path(__file__).parent.parent}/venv/lib/python3.8/site-packages')
```
- Extensions to auto-generate doc_generator.
```
extensions = [
    'sphinx.ext.napoleon',  # certain styles of doc strings
    'sphinx.ext.autodoc'  # generates from doc strings
]
```
-->
