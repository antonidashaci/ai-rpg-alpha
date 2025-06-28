"""Compile Twine .twee files under story/twine into JSON for the engine.

This is a stub that expects `twine2json` (npm) or the python package `twee2json`.
You can run:
    $ python scripts/compile_story.py
and it will produce JSON files inside `story/compiled/`.

Currently it simply copies `.twee` files to the compiled folder as placeholders.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TWINE_DIR = ROOT / "story" / "twine"
OUT_DIR = ROOT / "story" / "compiled"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def main() -> None:
    for twee in TWINE_DIR.glob("*.twee"):
        # Placeholder: copy to output with .json extension containing raw text
        data = {"raw": twee.read_text(encoding="utf-8")}
        out_path = OUT_DIR / f"{twee.stem}.json"
        out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"Compiled {twee.name} -> {out_path.relative_to(ROOT)} (stub)")

if __name__ == "__main__":
    main() 