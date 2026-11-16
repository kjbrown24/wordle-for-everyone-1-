#!/bin/bash
# Starts Wordle for Everyone: trains Rasa if needed, then runs
# the game page (port 8000) and the Rasa bot (port 5005).

if [ -z "$RASA_LICENSE" ]; then
  echo "RASA_LICENSE is not set. Add it as a Codespaces secret (see README), then restart the codespace."
  exit 1
fi

if ! ls models/*.tar.gz >/dev/null 2>&1; then
  echo "Training the bot (first time only, about a minute)..."
  rasa train
fi

echo "Starting the game page on port 8000..."
python -m http.server 8000 --directory web > /tmp/web.log 2>&1 &

echo "Starting Rasa on port 5005..."
rasa run --enable-api --cors "*"
