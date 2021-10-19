from setuptools import setup

setup(
    entry_points={
        'console_scripts': [
            'insta = insta.cli:main'
        ]
    }
)
