#!/bin/sh
set -e
TARGET="/usr/lib/enigma2/python/Plugins/Extensions/ArabyVUPanel"
SRC="$(dirname "$0")/usr/lib/enigma2/python/Plugins/Extensions/ArabyVUPanel"

if [ "$(id -u)" != "0" ]; then
    echo "Please run as root."
    exit 1
fi

if [ ! -f "$SRC/plugin.py" ]; then
    echo "plugin.py not found. Run this installer from the extracted package folder."
    exit 1
fi

mkdir -p "$TARGET"
cp "$SRC/plugin.py" "$TARGET/plugin.py"
chmod 644 "$TARGET/plugin.py"
echo "ARABY VU PANEL installed."
echo "Restart the Enigma2 GUI to see it under Plugins."
