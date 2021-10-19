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
`insta --help` - Help information.

`insta dp --profile <username>`
<br>
`insta dp` - Prompts to provide username.

`insta followers` - Prints followers' username and bio.

`insta followees` - Prints followees' username and bio.

`insta ungrateful --them` - Prints who don't follow you back.
<br>
`insta ungrateful --me` - Prints who you don't follow back.

### Commit
`pip3 install -r requirements.txt` - This installs `pre-commit` for linting and `sphinx` for auto-doc generation.

Linting:
<br>
PreCommit will ensure linting, and the doc creation are run on every commit.

Requirement:
<br>
pip install --no-cache --upgrade sphinx pre-commit recommonmark

Usage:
<br>
pre-commit run --all-files

### Links
[Repository](https://github.com/thevickypedia/instagram)

[Runbook](https://thevickypedia.github.io/instagram/)
