from setuptools import setup

setup(
    entry_points={
        'console_scripts': [
            'instagram = insta.cli:main'
        ]
    }
)
