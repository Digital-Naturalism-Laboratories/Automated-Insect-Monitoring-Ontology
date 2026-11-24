#!/usr/bin/env python3
"""Copy device-types.json into the tools that carry their own copy.

Run after editing device-types.json:

    python3 device-types/sync-copies.py           # copy
    python3 device-types/sync-copies.py --check   # only report which copies differ

Expects the other repos next to this one (~/Documents/GitHub/...). Standard library only.
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GITHUB = HERE.parent.parent
SOURCE = HERE / "device-types.json"

JSON_COPIES = [
    GITHUB / "mothbot-classify" / "src" / "config" / "device-types.json",
    GITHUB / "Mothbot_Process" / "assets" / "device-types.json",
]
# The firmware settings editor is one self-contained HTML file, so the list is embedded.
FIRMWARE_EDITOR = GITHUB / "Mothbox_Firmware" / "mothbox_custom_Unified" / "mothbox_settings_editor.html"
EMBEDDED = re.compile(r"(const STANDARD_DEVICE_TYPES = )\[.*?\n\];", re.S)
EMBEDDED_CHOICES = re.compile(r"(const DEVICE_CHOICES = )\{.*?\n\};", re.S)


def main():
    check_only = "--check" in sys.argv
    text = SOURCE.read_text(encoding="utf-8")
    data = json.loads(text)  # fails loudly on a JSON mistake
    types = data["deviceTypes"]
    choices = data.get("choices", {})
    different = 0

    for path in JSON_COPIES:
        if not path.parent.is_dir():
            print(f"skip (repo not found): {path}")
            continue
        if path.exists() and path.read_text(encoding="utf-8") == text:
            print(f"same:    {path}")
            continue
        different += 1
        if check_only:
            print(f"differs: {path}")
        else:
            path.write_text(text, encoding="utf-8")
            print(f"copied:  {path}")

    if FIRMWARE_EDITOR.exists():
        html = FIRMWARE_EDITOR.read_text(encoding="utf-8")
        if not EMBEDDED.search(html) or not EMBEDDED_CHOICES.search(html):
            print(f"!! couldn't find STANDARD_DEVICE_TYPES or DEVICE_CHOICES in {FIRMWARE_EDITOR}")
            return 1
        updated = EMBEDDED.sub(lambda m: m.group(1) + json.dumps(types, indent=2, ensure_ascii=False) + ";", html, count=1)
        updated = EMBEDDED_CHOICES.sub(lambda m: m.group(1) + json.dumps(choices, indent=2, ensure_ascii=False) + ";", updated, count=1)
        if updated == html:
            print(f"same:    {FIRMWARE_EDITOR}")
        else:
            different += 1
            if check_only:
                print(f"differs: {FIRMWARE_EDITOR}")
            else:
                FIRMWARE_EDITOR.write_text(updated, encoding="utf-8")
                print(f"copied:  {FIRMWARE_EDITOR}")
    else:
        print(f"skip (repo not found): {FIRMWARE_EDITOR}")

    print(f"{len(types)} device types; {different} cop{'y' if different == 1 else 'ies'} {'differ' if check_only else 'updated'}.")
    return 1 if check_only and different else 0


if __name__ == "__main__":
    sys.exit(main())
