# Instagram
Python script to retrieve data from Instagram

## Usage
### Env Variables:
```
export insta_user=<username>
export insta_pass=<password>
```
### Setup
`pip install .` - This installs the `instagram` package along with its requirements to use the CLI commands.

### CLI
`instagram --help` - Help information.

`instagram dp --target-profile <username>`
<br>
`instagram dp` - Prompts to provide username.

`instagram followers` - Prints followers' username and bio.

`instagram followees` - Prints followees' username and bio.

`instagram ungrateful --them=True` - Prints who don't follow you back.
<br>
`instagram ungrateful --me=True` - Prints who you don't follow back.

### Commit
`pip3 install -r requirements.txt` - This installs `pre-commit` for linting and `sphinx` for auto-doc generation.

`pre-commit run --all-files` - This will ensure linting and generates docs from docstrings.

### Runbook
https://thevickypedia.github.io/instagram/

<!--
## Replicate auto generation of pages
`pip3 install sphinx`<br>
`cd doc_generator`<br>
`sphinx-quickstart`<br>
### Addition to index.rst
```reStructuredText
.. automodule:: instagram.ig_connector
   :members:
   :undoc-members:
```
### Modifications to conf.py
- Insert and append file path for entry point script and libraries.
```python
import os
import sys
from pathlib import Path
sys.path.insert(0, os.path.abspath('../..'))
sys.path.append(f'{Path(__file__).parent.parent}/venv/lib/python3.8/site-packages')
```
- Extensions to auto-generate doc_generator.
```python
extensions = [
    'sphinx.ext.napoleon',  # certain styles of doc strings
    'sphinx.ext.autodoc'  # generates from doc strings
]
```
- HTML theme output
```
# https://www.sphinx-doc.org/en/master/usage/theming.html#builtin-themes
html_theme = 'agogo'
```

<details>
<sumary>gen_docs.sh</sumary>

```bash
#!/usr/bin/env bash
# set -e stops the execution of a script if a command or pipeline has an error.<br>
# This is the opposite of the default shell behaviour, which is to ignore errors in scripts.
set -e
rm -rf docs
mkdir docs
shopt -s dotglob nullglob  # https://www.gnu.org/software/bash/manual/bash.html#The-Shopt-Builtin
cd doc_generator && make html && mv _build/html/* ../docs
touch ../docs/.nojekyll
git add ../docs
```

</details>

-->
