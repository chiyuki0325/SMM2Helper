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
for file in "SMM2" "web" "config.py" "tgrcode_api.py" "widgets.py" "smm2helper.py" "README.md"; do
    cp -r "$file" "${RELEASE_DIR}/${file}"
done

msg "Applying default settings..."
sed -i '/SAVE_DIR/c\SAVE_DIR: str = "SMM2 save data directory path"' "${RELEASE_DIR}/config.py"
sed -i '/DEBUG/c\DEBUG: bool = False' "${RELEASE_DIR}/config.py"
sed -i '/TGRCODE_API_COURSE_NUMBER/c\TGRCODE_API_COURSE_NUMBER: int = 20' "${RELEASE_DIR}/config.py"
sed -i '/SHOW_EMPTY_SLOT/c\SHOW_EMPTY_SLOT: bool = True' "${RELEASE_DIR}/config.py"
sed -i '/LOAD_ONLINE_ON_START/c\LOAD_ONLINE_ON_START: bool = True' "${RELEASE_DIR}/config.py"
sed -i '/SHOW_THUMBNAILS/c\SHOW_THUMBNAILS: bool = True' "${RELEASE_DIR}/config.py"

rm -rf "${RELEASE_DIR}/SMM2/__pycache__"

cp requirements-linux.txt "${RELEASE_DIR}/requirements.txt"
cp smm2helper-linux.sh "${RELEASE_DIR}/smm2helper"

msg "Creating final package..."
pushd "$RELEASE_DIR"
tar -czvf "../SMM2Helper-${VERSION}-linux.tar.gz" *
popd

rm -rf "$RELEASE_DIR"
