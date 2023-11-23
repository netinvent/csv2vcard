#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of csv2vcard package


import sys
import os
import pkg_resources
import setuptools

PACKAGE_NAME="csv2vcard"
DESCRIPTION="CLI tool to convert CSV files into vcards"


def _read_file(filename):
    here = os.path.abspath(os.path.dirname(__file__))
    if sys.version_info[0] < 3:
        # With python 2.7, open has no encoding parameter, resulting in TypeError
        # Fix with io.open (slow but works)
        from io import open as io_open

        try:
            with io_open(
                os.path.join(here, filename), "r", encoding="utf-8"
            ) as file_handle:
                return file_handle.read()
        except IOError:
            # Ugly fix for missing requirements.txt file when installing via pip under Python 2
            return ""
    else:
        with open(os.path.join(here, filename), "r", encoding="utf-8") as file_handle:
            return file_handle.read()


def get_metadata(package_file):
    """
    Read metadata from package file
    """

    _metadata = {}

    for line in _read_file(package_file).splitlines():
        if line.startswith("__version__") or line.startswith("__description__"):
            delim = "="
            _metadata[line.split(delim)[0].strip().strip("__")] = (
                line.split(delim)[1].strip().strip("'\"")
            )
    return _metadata


def parse_requirements(filename):
    """
    There is a parse_requirements function in pip but it keeps changing import path
    Let's build a simple one
    """
    try:
        requirements_txt = _read_file(filename)
        install_requires = [
            str(requirement)
            for requirement in pkg_resources.parse_requirements(requirements_txt)
        ]
        return install_requires
    except OSError:
        print(
            'WARNING: No requirements.txt file found as "{}". Please check path or create an empty one'.format(
                filename
            )
        )


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

package_path = os.path.abspath(PACKAGE_NAME)
for path in ["__main__.py", PACKAGE_NAME + ".py"]:
    package_file = os.path.join(package_path, "__main__.py")
    if os.path.isfile(package_file):
        break
metadata = get_metadata(package_file)
requirements = parse_requirements(os.path.join(package_path, "requirements.txt"))
long_description = _read_file("README.md")

if os.name == "nt":
  scripts = ["misc/csv2vcard.cmd"]
  console_scripts = []
else:
  scripts = []
  console_scripts = ["csv2vcard = csv2vcard.__main__:main"]

setuptools.setup(
  name = PACKAGE_NAME,
  packages=setuptools.find_packages(),
  version=metadata["version"],
  install_requires=requirements,
  description = DESCRIPTION,
  long_description = long_description,
  long_description_content_type='text/markdown',
  author = 'NetInvent & ReallyCoolData & Nikolay Dimolarov',
    author_email="contact@netinvent.fr",
  url = 'https://github.com/netinvent/csv2vcard', 
  keywords = ['csv', 'vcard', 'export', 'conversion', 'mass'],
  python_requires = '>=3.6',
  classifiers = [
    'Development Status :: 4 - Beta','License :: OSI Approved :: MIT License',
    "Intended Audience :: System Administrators",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Developers",
    'Programming Language :: Python :: 3.6',
    "Topic :: Utilities",
    ],
  python_requires=">=3.6",
  scripts=scripts,
  entry_points={
     "console_scripts": console_scripts,
  }
)
