@echo off
title 3C's ERP System
echo ================================================
echo    3C's ERP System - Starting...
echo ================================================
echo.

:: Start Django server minimized
echo [1/2] Starting Django server...
start /min "Django Server" cmd /k "cd /d "C:\Users\bnext01\OneDrive - bneXt Inc\Documents\Python\3cs_erp_web" && python manage.py runserver 0.0.0.0:8000"

:: Wait for Django to start
timeout /t 5 /nobreak > nul

:: Start Cloudflare tunnel minimized
echo [2/2] Starting Cloudflare tunnel...
start /min "Cloudflare Tunnel" cmd /k "cd /d C:\CloudFlared && cloudflared-windows-amd64.exe tunnel --url http://localhost:8000"

echo.
echo ================================================
echo    All services started and minimized!
echo    Check taskbar for Cloudflare URL
echo ================================================
timeout /t 3 /nobreak > nul
exit