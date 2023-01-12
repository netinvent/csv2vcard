import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
  name = 'csv2vcard',
  packages = ['csv2vcard'],
  version = '0.3.0',
  description = 'A library for converting csvs to vCards',
  long_description = README,
  long_description_content_type='text/markdown',
  author = 'ReallyCoolData',
  author_email = 'N/A',
  url = 'https://github.com/ReallyCoolData/csv2vcard', 
  download_url = 'https://github.com/ReallyCoolData/csv2vcard/archive/refs/tags/0.2.3.tar.gz',
  keywords = ['csv', 'vcard', 'export'],
  python_requires = '>=3.6',
  classifiers = [
    'Development Status :: 3 - Alpha','License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    ],
)
