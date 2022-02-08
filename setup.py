"""
Setup file and install script for TextEncrypt.

Version 0.3.4 (Feb. 8, 2022)
Copyright (c) 2022 Chengrui Wang
"""
import os
from argparse import Namespace

try:
    from setuptools import setup, find_packages

    _has_setuptools = True
except ImportError:
    from distutils.core import setup, find_packages

DESCRIPTION = "TextEncrypt: encrypt and decrypt the text of a file"

meta = Namespace(
    __DISTNAME__="TextEncrypt",
    __AUTHOR__="Chengrui Wang",
    __AUTHOR_EMAIL__="aiyacharley@outlook.com",
    __URL__="https://github.com/aiyacharley/TextEncrypt",
    __LICENSE__="BSD (3-clause)",
    __DOWNLOAD_URL__="https://github.com/aiyacharley/TextEncrypt",
    __VERSION__="0.3.4",
)

if __name__ == "__main__":

    THIS_PATH = os.path.abspath(os.path.dirname(__file__))
    long_description = os.path.join(THIS_PATH, "README.md")

    setup(name=meta.__DISTNAME__,
          version=meta.__VERSION__,
          author=meta.__AUTHOR__,
          author_email=meta.__AUTHOR_EMAIL__,
          maintainer=meta.__AUTHOR__,
          maintainer_email=meta.__AUTHOR_EMAIL__,
          description=DESCRIPTION,
          long_description=(open(long_description).read()),
          long_description_content_type="text/markdown",
          license=meta.__LICENSE__,
          url=meta.__URL__,
          download_url=meta.__URL__,
          packages=find_packages(),
          include_package_data=True,
          install_requires=[
              "pycryptodome"
          ],
          entry_points={
              "console_scripts": [
                  "TextEncrypt = TextEncrypt.AES_encrypt:TextEncrypt"
              ]
          },
          classifiers=[
              "Intended Audience :: Science/Research",
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: BSD License",
              "Topic :: Security",
              "Topic :: Text Processing",
              "Operating System :: Microsoft :: Windows"],
          )
