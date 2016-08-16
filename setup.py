import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "lucid_utils",
    version = "1.0",
    author = "Cal Hewitt",
    author_email = "hello@calhewitt.xyz",
    description = ("A library for analysing LUCID data"),
    license = "MIT",
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
