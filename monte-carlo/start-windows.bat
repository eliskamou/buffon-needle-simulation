@echo off
rem Monte Carlo pi - full-screen kiosk launch (Windows). Double-click this file.
rem Quit with Alt+F4.
set "FILE=%~dp0index.html"
rem A separate profile forces a fresh browser window even if the browser is already open.
set "PROFILE=%TEMP%\buffon-kiosk"

for %%B in (
  "%ProgramFiles%\Google\Chrome\Application\chrome.exe"
  "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
  "%LocalAppData%\Google\Chrome\Application\chrome.exe"
  "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
  "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
) do (
  if exist %%B (
    start "" %%B --kiosk "%FILE%" --edge-kiosk-type=fullscreen --user-data-dir="%PROFILE%" --no-first-run --no-default-browser-check --disable-features=Translate --autoplay-policy=no-user-gesture-required
    exit /b
  )
)

rem No Chrome/Edge found: open normally, then press F in the app for fullscreen.
start "" "%FILE%"
