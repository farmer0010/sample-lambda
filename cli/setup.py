from setuptools import find_packages, setup

setup(
    name="mylog",
    version="0.1.0",
    packages=find_packages(include=["cli", "cli.*"]),
    install_requires=[
        "requests",
        "keyring",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "mylog=cli.adapters.inbound.cli_adapter:main",
        ],
    },
)
