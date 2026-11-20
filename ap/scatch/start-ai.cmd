@echo off
cd /d "%~dp0"
if not exist ".env" (
  echo Le fichier .env est absent.
  echo Copie .env.example vers .env et ajoute ta cle API Gemini.
  pause
  exit /b 1
)
node --env-file=.env server.mjs
pause
