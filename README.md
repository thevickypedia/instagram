# Instagram
Python script to retrieve data from Instagram

### Env Variables
```
export insta_user=<username>
export insta_pass=<password>
```
Optionally environment variables can be loaded from a `.env` file using the python_dotenv module.

### Setup
`pip install .` - This installs the `instagram` package along with its requirements to use the CLI commands.

### CLI
- `insta --help` - Help information.
- `insta dp --profile <username>`
- `insta dp` - Prompts to provide username.
- `insta followers` - Prints followers' username and bio.
- `insta followees` - Prints followees' username and bio.
- `insta ungrateful --them` - Prints you follow who don't follow you back.
- `insta ungrateful --me` - Prints followers who you don't follow back.

### Coding Standards
Docstring format: [`Google`](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) <br>
Styling conventions: [`PEP 8`](https://www.python.org/dev/peps/pep-0008/) <br>
Clean code with pre-commit hooks: [`flake8`](https://flake8.pycqa.org/en/latest/) and 
[`isort`](https://pycqa.github.io/isort/)

### [Release Notes](https://github.com/thevickypedia/Jarvis_UI/blob/main/release_notes.rst)
**Requirement**
```shell
python -m pip install changelog-generator
```

**Usage**
```shell
changelog reverse -f release_notes.rst -t 'Release Notes'
```

### Linting
`PreCommit` will ensure linting, and the doc creation are run on every commit.

**Requirement**
<br>
```bash
pip install --no-cache sphinx==5.1.1 pre-commit recommonmark
```

**Usage**
<br>
```bash
pre-commit run --all-files
```

### Runbook
[![made-with-sphinx-doc](https://img.shields.io/badge/Code%20Docs-Sphinx-1f425f.svg)](https://www.sphinx-doc.org/en/master/man/sphinx-autogen.html)

[https://thevickypedia.github.io/instagram/](https://thevickypedia.github.io/instagram/)
