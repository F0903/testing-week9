# PDF Downloader

## Prerequisites

To run the project simply first create a new virtual environment

```
python -m venv .venv
```

for windows (if using PowerShell) make sure that LocalMachine execution policy is set to AllSigned

```
Set-ExecutionPolicy -ExecutionPolicy AllSigned -Scope LocalMachine
```

then run

```
./.venv/Scripts/activate
```

for windows (PowerShell) or

```
. .venv/bin/activate
```

for macos or linux (bash)
then

```
pip install -r requirements.txt
```

## Usage

### Run with default values

```
python -m src.main
```

### Overwrite parameters

1. `-h` Shows a help of the overwrite parameters
2. `-d` Overwrite default directory
3. `-rf` Overwrites the default report file destination and name
4. `-uf` Overwrites the default filename with url links. For now it must have the following coloumns : `BRNum, pdf_url, Report Html Address`
5. `-t` Overwrites number of threads

I have no speficic points I want you to look at for feedback, so just find what you deem the most necesarry

## WEEK 9 CHANGES

- Fixed and updated requirements.txt
- Deleted unused FileHandler.py
- Fixed class and file naming
- Removed explicit inheritance from object
- Moved the "main function" to its own main.py
- Moved source files to "src" directory
