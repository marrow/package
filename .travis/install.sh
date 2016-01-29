#!/bin/bash
set -e
set -x

git config --global user.email "alice+travis@gothcandy.com"
git config --global user.name "Travis: Marrow"

pip install --upgrade setuptools pip
pip install --upgrade pytest
pip install tox
pip install tox-travis
pip install codecov
pip install pytest-cov
pip install pytest-flakes
pip install pytest-spec
