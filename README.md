# ARABY VU PANEL

A starter Enigma2 plugin for Vu+ Zero 4K running OpenATV 8.x.

## Features in this starter build
- Appears in the Plugins menu.
- Arabic/English menu toggle (press MENU).
- Receiver information screen.
- Opens the image's Plugin Manager.
- GUI restart with confirmation.
- Black and gold interface.

## Compatibility
Designed for Enigma2 / OpenATV 8.x. Enigma2 images vary, so test on the receiver before relying on it. Arabic glyph shaping and right-to-left layout depend on the installed image fonts and skin renderer.

## Install from USB / SSH
Copy the `usr` directory to the receiver's root filesystem, preserving paths:

`/usr/lib/enigma2/python/Plugins/Extensions/ArabyVUPanel/plugin.py`

Then restart Enigma2 GUI from the receiver menu, or reboot.

Example with SCP from a computer:
`scp -r usr root@RECEIVER_IP:/`

## Important
- This is an initial safe starter version, not a full system-management panel.
- The "Update package lists" item runs `opkg update` only after confirmation.
- Do not install scripts from sources you do not trust.
- Keep a backup of your settings before experimenting.
