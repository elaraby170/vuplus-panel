#!/bin/sh
set -e
TARGET="/usr/lib/enigma2/python/Plugins/Extensions/ArabyVUPanel"
if [ "$(id -u)" != "0" ]; then
    echo "Please run as root."
    exit 1
fi
rm -rf "$TARGET"
echo "ARABY VU PANEL removed. Restart Enigma2 GUI."
