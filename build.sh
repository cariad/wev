#!/bin/bash -e
rm -rf dist
python setup.py bdist_wheel
rm -rf build
mkdocs build
