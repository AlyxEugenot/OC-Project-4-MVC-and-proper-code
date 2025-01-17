from setuptools import setup

setup(
    name="view_tuto",
    version="0.1.0",
    py_modules=["src"],
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "start_up = src:start_app"
            "to_write_in_cmd = src:func",
            "hello_world = src:hello_world",
        ],
    },
)
