# CSM parser
[![GitHub Pipenv locked Python version (branch)](https://img.shields.io/github/pipenv/locked/python-version/ihor-voronin/csm_parser/master?logo=python&logoColor=FBE072)](https://github.com/ihor-voronin/csm_parser/blob/master/Pipfile)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![GitHub contributors](https://img.shields.io/github/contributors/ihor-voronin/csm_parser?logo=github)](https://github.com/ihor-voronin/csm_parser/graphs/contributors)
[![GitHub commits since latest release (by SemVer including pre-releases)](https://img.shields.io/github/commits-since/ihor-voronin/csm_parser/latest?include_prereleases&logo=github)](https://github.com/ihor-voronin/csm_parser/releases/latest)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ihor-voronin/csm_parser/CodeQL?label=checks&logo=github)](https://github.com/ihor-voronin/csm_parser/blob/master/.github/workflows/codeql.yml)
![Code platform](https://img.shields.io/badge/platform-windows-blue?logo=windows)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0f4fe4e481354b2ab38e2d3385587821)](https://www.codacy.com/gh/ihor-voronin/csm_parser/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ihor-voronin/csm_parser&amp;utm_campaign=Badge_Grade)
[![Libraries.io dependency status for GitHub repo](http://144.217.6.255/librariesio/github/ihor-voronin/csm_parser)](https://libraries.io/github/ihor-voronin/csm_parser)

## Install dev version

### Install environment
Create a command line entry point `pipenv` as a `dev`
```bash
> pipenv sync --dev 
```

### Install pre-commit

Install `pre-commit` tools:
```bash
> pre-commit install 
```

## Install build version

### Rules of installation
TODO

## How to use

### 1. Get ID of open window with  Cyber Station Manager

**In Dev version**

Command:
```bash
> python ./main.py  --windows-list
```
Example output:
```bash
> python ./main.py --windows-list
List of open windows with their IDs
window_id        window_name
    132664 -- Basic Syntax | Markdown Guide - Google Chrome
     72468 -- Documents
    590570 -- Cyber Station Manager - [ Nhan vien: ADMIN (Admin) ]
    459906 -- Microsoft Text Input Application
    131438 -- Program Manager
```
In this case **ID** of **Cyber Station Manager** will be **590570**

**In Build version** Command:
```bash
> .\main.exe --windows-list
```
Example output:
```bash
> .\main.exe --windows-list
List of open windows with their IDs
window_id        window_name
    525820 -- Cyber Station Manager - [ Nhan vien: ADMIN (Admin) ]
    459906 -- Microsoft Text Input Application
    131438 -- Program Manager
```
In this case **ID** of **Cyber Station Manager** will be **525820**


### 2. Check settings and set correct value

**In Dev version**

Command for display current settings:
```bash
> python ./main.py --display-settings
```
Example output:
```bash
> python ./main.py --display-settings

Current settings:

{
    "PgDn_contain_nickname": 13,
    "PgDn_count_in_full_page": 13,
    "PgDn_count_in_last_page": 3,
    "PgDn_remain_count_nickname": 5,
    "folder_save_processed": "CSM_parser_processed",
    "folder_save_screenshot": "CSM_parser_screenshot",
    "folder_save_temp": "CSM_parser_temp",
    "name_pattern": "CSM-{name}-{timestamp}",
    "page_count": 16,
    "page_nickname_height": 28,
    "page_nickname_width": 600,
    "page_start_coordinate_nickname_x": 13,
    "page_start_coordinate_nickname_y": 255,
    "start_coordinate_x": 0,
    "start_coordinate_y": 0,
    "templates_is_local": false,
    "templates_local_file": "templates.json",
    "templates_url": "https://raw.githubusercontent.com/ihor-voronin/csm_parser/master/templates.json",
    "window_height": 700,
    "window_width": 1200
}
```

**In Build version**

Command for display current settings:
```bash
> .\main.exe  --display-settings
```
Example output:
```bash
> .\main.exe  --display-settings

Current settings:

{
    "PgDn_contain_nickname": 13,
    "PgDn_count_in_full_page": 13,
    "PgDn_count_in_last_page": 3,
    "PgDn_remain_count_nickname": 5,
    "folder_save_processed": "CSM_parser_processed",
    "folder_save_screenshot": "CSM_parser_screenshot",
    "folder_save_temp": "CSM_parser_temp",
    "name_pattern": "CSM-{name}-{timestamp}",
    "page_count": 16,
    "page_nickname_height": 28,
    "page_nickname_width": 600,
    "page_start_coordinate_nickname_x": 13,
    "page_start_coordinate_nickname_y": 255,
    "start_coordinate_x": 0,
    "start_coordinate_y": 0,
    "templates_is_local": false,
    "templates_local_file": "templates.json",
    "templates_url": "https://raw.githubusercontent.com/ihor-voronin/csm_parser/master/templates.json",
    "window_height": 700,
    "window_width": 1200
}
```

Detailed information about the settings [HERE](https://todo.com).
