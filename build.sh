#!/bin/bash -e
echo "${1:?}" > wev/VERSION
rm -rf dist
python setup.py bdist_wheel
rm -rf build
mkdocs build
