@echo off
title Servidor Local com Sincronizacao em Tempo Real
chcp 65001 >nul
echo ========================================================
echo   CAPIVARA CLUB HOT - LOCAL CLONE COM SYNC EM TEMPO REAL
echo ========================================================
echo.
echo Iniciando servidor em http://localhost:5500 ...
start "" http://localhost:5500/paginas/painel.html
python -u scripts\server.py
pause
