#!/bin/bash
# Monte Carlo pi – full-screen kiosk launch (macOS). Double-click this file.
# Quit with Cmd+Q.
DIR="$(cd "$(dirname "$0")" && pwd)"
FILE="$DIR/index.html"
# A separate profile forces a fresh browser window even if the browser is already open.
PROFILE="${TMPDIR:-/tmp}/buffon-kiosk"

for APP in "Google Chrome" "Microsoft Edge" "Chromium" "Brave Browser"; do
  if [ -d "/Applications/$APP.app" ] || [ -d "$HOME/Applications/$APP.app" ]; then
    open -na "$APP" --args --kiosk "$FILE" \
      --user-data-dir="$PROFILE" --no-first-run --no-default-browser-check \
      --disable-features=Translate --autoplay-policy=no-user-gesture-required
    exit 0
  fi
done

# No Chromium-based browser: open normally, then press F in the app for fullscreen.
open "$FILE"
