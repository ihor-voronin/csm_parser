## How to create and run .exe file

### 1. Install pyinstaller

Command:
```bash
> pip install pyinstaller
```
### 2. Create .exe file

Command:
```bash
>  pyinstaller -F -n csm_parser --console main.py
```

### 3. Open .exe file
Run PowerShell as Administrator and navigate to the folder where is the project csm_parser.

Command:
```bash
>  cd <path to destination folder>
```

Then go to the folder dist

Command:
```bash
>  cd .\dist\
```
Run csm_parser.exe file and enter following arguments: your database_password, page_count and page_last_nickname_count

Command:
```bash
>  .\csm_parser.exe --database_password  [your_database_password] --page_count [number_of_page] --page_last_nickname_count [number_of_page_last_nickname]
```