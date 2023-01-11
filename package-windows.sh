#!/usr/bin/env bash

# SMM2Helper Windows release script

RELEASE_DIR=release-windows

function msg() {
    echo -e "\033[1;34m::\033[1;0m ${1}\033[0m"
}

VERSION="$(python -c 'import config; print(config.VERSION, end="")')"

msg "Packaging for Windows release ${VERSION}..."

if [ ! -f "WindowsLauncher/SMM2Helper.exe" ]; then
    error "Please compile the launcher first!"
    exit 1
fi

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
sed -i '/SHOW_EMPTY_SLOT/c\SHOW_EMPTY_SLOT: bool = False' "${RELEASE_DIR}/config.py"
sed -i '/LOAD_ONLINE_ON_START/c\LOAD_ONLINE_ON_START: bool = True' "${RELEASE_DIR}/config.py"
sed -i '/SHOW_THUMBNAILS/c\SHOW_THUMBNAILS: bool = False' "${RELEASE_DIR}/config.py"

rm -rf "${RELEASE_DIR}/SMM2/__pycache__"

cp requirements-windows.txt "${RELEASE_DIR}/requirements.txt"
cp WindowsLauncher/SMM2Helper.exe "${RELEASE_DIR}/SMM2Helper.exe"

msg "Creating final package..."
7z a "SMM2Helper-${VERSION}-windows.zip" ./$RELEASE_DIR/* -mx9

rm -rf "$RELEASE_DIR"

