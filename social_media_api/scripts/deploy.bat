@echo off
echo Starting deployment process...

REM Load environment variables from file
if exist ..\.env.production (
    for /f "usebackq tokens=*" %%i in ("..\.env.production") do (
        set %%i
    )
)

echo Installing dependencies...
pip install -r ..\requirements.txt

echo Running migrations...
python ..\manage.py migrate

echo Collecting static files...
python ..\manage.py collectstatic --noinput

echo Deployment completed successfully!
pause