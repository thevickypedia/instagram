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
`instagram --help` - Help information.

`instagram dp --profile <username>`
<br>
`instagram dp` - Prompts to provide username.

`instagram followers` - Prints followers' username and bio.

`instagram followees` - Prints followees' username and bio.

`instagram ungrateful --them` - Prints who don't follow you back.
<br>
`instagram ungrateful --me` - Prints who you don't follow back.

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
