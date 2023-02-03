for /F %%i in ('python -c "import config; print(config.VERSION, end="")"') do ( set version=%%i)
pyinstaller -y -F -n SMM2Helper -w -i res/smm2helper.ico --add-data web;web --uac-admin smm2helper.py
copy config.yml dist/
copy README.md dist/
copy LICENSE dist/
7z a -tzip SMM2Helper-%version%-windows-bundle.zip dist/*
rd /s /q dist
rd /s /q build
