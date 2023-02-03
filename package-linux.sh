#!/usr/bin/env bash

# SMM2Helper Linux release script

RELEASE_DIR=release-linux

function msg() {
    echo -e "\033[1;34m::\033[1;0m ${1}\033[0m"
}

VERSION="$(python -c 'import config; print(config.VERSION, end="")')"

msg "Packaging for Linux release ${VERSION}..."

msg "Preparing files..."
./download-requirements.sh

if [ ! -d "$RELEASE_DIR" ]; then mkdir "$RELEASE_DIR"; fi

msg "Copying files..."
for file in "SMM2" "web" "config.yml" "tgrcode_api.py" "widgets.py" "smm2helper.py" "README.md" "LICENSE"; do
    cp -r "$file" "${RELEASE_DIR}/${file}"
done

rm -rf "${RELEASE_DIR}/SMM2/__pycache__"

cp requirements-linux.txt "${RELEASE_DIR}/requirements.txt"
cp smm2helper-linux.sh "${RELEASE_DIR}/smm2helper"

msg "Creating final package..."
pushd "$RELEASE_DIR"
tar -czvf "../SMM2Helper-${VERSION}-linux-standalone.tar.gz" *
popd

rm -rf "$RELEASE_DIR"
