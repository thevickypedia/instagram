#!/usr/bin/env bash
# `set -e` stops the execution of a script if a command or pipeline has an error.
# This is the opposite of the default shell behaviour, which is to ignore errors in scripts.
set -e
rm -rf docs
mkdir docs
shopt -s dotglob nullglob  # https://www.gnu.org/software/bash/manual/bash.html#The-Shopt-Builtin
cd doc_generator && make html && mv _build/html/* ../docs
touch ../docs/.nojekyll
git add ../docs