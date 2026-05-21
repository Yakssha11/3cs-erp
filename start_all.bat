@echo off
title 3C's ERP System
echo ================================================
echo    3C's ERP System - Starting...
echo ================================================
echo.

:: Start MySQL check
echo [1/3] Checking MySQL...
timeout /t 2 /nobreak > nul

:: Start Django server
echo [2/3] Starting Django server...
start "Django Server" cmd /k "cd /d "C:\Users\bnext01\OneDrive - bneXt Inc\Documents\Python\3cs_erp_web" && python manage.py runserver 0.0.0.0:8000"

:: Wait for Django to start
timeout /t 5 /nobreak > nul

:: Start Cloudflare tunnel
echo [3/3] Starting Cloudflare tunnel...
start "Cloudflare Tunnel" cmd /k "cd /d C:\CloudFlared && cloudflared-windows-amd64.exe tunnel --url http://localhost:8000"

echo.
echo ================================================
echo    All services started!
echo    Check the Cloudflare window for your URL
echo ================================================
timeout /t 3 /nobreak > nul