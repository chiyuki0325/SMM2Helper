#!/usr/bin/env bash

# SMM2Helper Linux release script

RELEASE_DIR=release-linux

function msg() {
    echo -e "\033[1;34m::\033[1;0m ${1}\033[0m"
}

msg "Packaging for Linux release..."

msg "Preparing files..."
./download-requirements.sh

if [ ! -d "$RELEASE_DIR" ]; then mkdir "$RELEASE_DIR"; fi

msg "Copying files..."
cp *.py "${RELEASE_DIR}"
for file in "SMM2" "web"; do
    cp -r "$file" "${RELEASE_DIR}/${file}"
done

rm -rf "${RELEASE_DIR}/SMM2/__pycache__"

cp requirements-linux.txt "${RELEASE_DIR}/requirements.txt"
cp smm2helper-linux.sh "${RELEASE_DIR}/smm2helper"

tar -czvf SMM2Helper-linux.tar.gz "$RELEASE_DIR/"*
rm -rf "$RELEASE_DIR"
