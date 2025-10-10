Write-Host "Starting deployment process..." -ForegroundColor Green

# Load environment variables
if (Test-Path "..\.env.production") {
    Get-Content "..\.env.production" | ForEach-Object {
        if ($_ -match "^(.*?)=(.*)$") {
            $key = $matches[1]
            $value = $matches[2]
            [Environment]::SetEnvironmentVariable($key, $value)
        }
    }
}

Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r ..\requirements.txt

Write-Host "Running migrations..." -ForegroundColor Yellow
python ..\manage.py migrate

Write-Host "Collecting static files..." -ForegroundColor Yellow
python ..\manage.py collectstatic --noinput

Write-Host "Deployment completed successfully!" -ForegroundColor Green
Read-Host "Press Enter to continue"