from setuptools import setup

setup(
    name='_view_tuto',
    version='0.1.0',
    py_modules=['src'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'to_write_in_cmd = src:func',
        ],
    },
)