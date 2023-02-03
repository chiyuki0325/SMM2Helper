#!/usr/bin/env bash

VERSION=$(python -c "import config; print(config.VERSION, end='')")
pyinstaller -y -F -n SMM2Helper -w --add-data web:web smm2helper.py
for file in "config.yml" "README.md" "LICENSE"; do
  cp "$file" "dist/"
done
tar -czvf "SMM2Helper-${VERSION}-linux-bundle.tar.gz" dist/
for file in "dist" "build"; do
  rm -rf "$file"
done