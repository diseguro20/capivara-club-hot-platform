@echo off
title Sincronizador Capivara Club Hot
chcp 65001 >nul
echo ========================================================
echo   SINCRONIZADOR EM TEMPO REAL - CAPIVARA CLUB HOT
echo ========================================================
echo.
python scripts\sync_engine.py
echo.
echo Pressione qualquer tecla para sair...
pause >nul
