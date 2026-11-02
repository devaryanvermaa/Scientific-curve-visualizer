@echo off
title GraphiX - Scientific Function Visualizer
echo Starting GraphiX...
python main.py
if errorlevel 1 (
    echo.
    echo An error occurred while launching the application.
    pause
)
