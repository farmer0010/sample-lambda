from setuptools import setup

setup(
    name="mylog",
    version="0.1.0",
    py_modules=["mylog"],
    install_requires=[
        "requests",
        "keyring",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "mylog=mylog:main",
        ],
    },
)
