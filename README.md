[![Run tests](https://github.com/F0903/testing-week9/actions/workflows/run-tests.yml/badge.svg)](https://github.com/F0903/testing-week9/actions/workflows/run-tests.yml)

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

for PowerShell or

```
. .venv/Scripts/activate
```

for bash
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
- Added test directory for tests
- Wrote tests for controller.py
- Fixed PolarFileHandler not preserving order in metadata output
- Wrote a "testing http server" to serve requests for the tests
- Wrote tests for downloader.py
- Wrote tests for polar_file_handler.py
- Uploaded the dataset for easy usage
- Embedded a PDF in B64 for easy sending via testing http server
- Wrote a test for the main function
- Fixed issue where the program would crash if all downloads in the dataset had already succeeded
