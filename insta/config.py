import os

import dotenv

if os.path.isfile('.env'):
    dotenv.load_dotenv(dotenv_path='.env', verbose=True, override=True)


class EnvConfig:
    """Load env variables.

    >>> EnvConfig

    """

    insta_user: str = os.environ.get('INSTA_USER') or os.environ.get('insta_user')
    insta_pass: str = os.environ.get('INSTA_PASS') or os.environ.get('insta_pass')


env = EnvConfig()

if not all((env.insta_user, env.insta_pass)) and not os.environ.get('pre_commit'):
    raise ValueError("Missing `insta_user` or `insta_pass`")
