#!/bin/bash
# Monte Carlo pi – full-screen kiosk launch (Linux). Run: ./start-linux.sh
# Quit with Alt+F4.
DIR="$(cd "$(dirname "$0")" && pwd)"
FILE="$DIR/index.html"
PROFILE="${TMPDIR:-/tmp}/buffon-kiosk"

for B in google-chrome google-chrome-stable chromium chromium-browser microsoft-edge brave-browser; do
  if command -v "$B" >/dev/null 2>&1; then
    exec "$B" --kiosk "$FILE" \
      --user-data-dir="$PROFILE" --no-first-run --no-default-browser-check \
      --disable-features=Translate --autoplay-policy=no-user-gesture-required
  fi
done

# No Chromium-based browser: open normally, then press F in the app for fullscreen.
xdg-open "$FILE"
