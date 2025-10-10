@echo off
echo Starting database backup...

REM Set backup directory
set BACKUP_DIR=C:\backups
if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

REM Get current date and time
for /f "tokens=1-3 delims=/" %%a in ('date /t') do (set DATE=%%c%%a%%b)
for /f "tokens=1-2 delims=:" %%a in ('time /t') do (set TIME=%%a%%b)
set TIMESTAMP=%DATE%_%TIME%

REM Backup PostgreSQL (if using PostgreSQL)
REM pg_dump %DATABASE_URL% > %BACKUP_DIR%\backup_%TIMESTAMP%.sql

REM For SQLite (copy the file)
if exist ..\db.sqlite3 (
    copy ..\db.sqlite3 %BACKUP_DIR%\backup_%TIMESTAMP%.sqlite3
    echo Backup created: backup_%TIMESTAMP%.sqlite3
) else (
    echo No SQLite database found
)

echo Backup process completed
pause