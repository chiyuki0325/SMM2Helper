#!/usr/bin/env bash

# SMM2Helper Linux start script

function command_exist() {
	local command="$1"
	command -v "${command}" >/dev/null 2>&1
}

function msg() {
    echo -e "\033[1;34m::\033[1;0m ${1}\033[0m"
}

function error() {
    echo -e "\033[31m${1}\033[0m"
}

if ! command_exist "python3"; then
    error "No Python 3 executable found, please install Python first."
    exit 1
fi

if [ -z "$SMM2HELPER_VENV_DIR" ]; then
    msg "Running in portable mode."
    SMM2HELPER_VENV_DIR="$PWD/venv"
fi

if ! [[ -d "$SMM2HELPER_VENV_DIR" || -f "${SMM2HELPER_VENV_DIR}/bin/activate" ]]; then
    msg "Creating virtual environment..."
    env python3 -m venv "$SMM2HELPER_VENV_DIR"

    msg "Installing packages..."
    source "${SMM2HELPER_VENV_DIR}/bin/activate"
    "${SMM2HELPER_VENV_DIR}/bin/pip" install -r requirements.txt
    "${SMM2HELPER_VENV_DIR}/bin/pip" uninstall -y setuptools
fi

source "${SMM2HELPER_VENV_DIR}/bin/activate"
env python3 "${PWD}/smm2helper.py"
