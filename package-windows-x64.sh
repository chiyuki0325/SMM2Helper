#!/usr/bin/env bash

# SMM2Helper Windows release script

RELEASE_DIR=release-windows-x64

function msg() {
    echo -e "\033[1;34m::\033[1;0m ${1}\033[0m"
}

msg "Packaging for Windows release..."

if [ ! -f "WindowsLauncher/SMM2Helper.exe" ]; then
    error "Please compile the launcher first!"
    exit 1
fi

msg "Preparing files..."
./download-requirements.sh

if [ ! -d "$RELEASE_DIR" ]; then mkdir "$RELEASE_DIR"; fi

msg "Copying files..."
cp *.py "${RELEASE_DIR}"
for file in "SMM2" "web"; do
    cp -r "$file" "${RELEASE_DIR}/${file}"
done

rm -rf "${RELEASE_DIR}/SMM2/__pycache__"

cp requirements-windows.txt "${RELEASE_DIR}/requirements.txt"
cp WindowsLauncher/SMM2Helper.exe "${RELEASE_DIR}/SMM2Helper.exe"

7z a SMM2Helper-windows-x64.zip ./$RELEASE_DIR/* -mx9
rm -rf "$RELEASE_DIR"

