#!/usr/bin/env python3
"""Pack the runtime skill files into a distributable zip.

Used to build the `anime-image-restyle-vX.Y.Z.zip` asset attached to each
GitHub Release. Only files the skill actually needs at runtime are included —
repo housekeeping (.github/, CHANGELOG.md, this script, dist/, outputs/) is
deliberately left out so the archive drops cleanly into a skills directory.

The version is read from the `version:` field in SKILL.md frontmatter, so
bumping the version there is the only step needed before tagging a release.

Usage:
    python scripts/package.py
    python scripts/package.py --version 1.2.0      # override the version
    python scripts/package.py --output-dir build   # override output location

Stdlib only, no dependencies. Exit code 0 on success, 1 on failure.
"""

import argparse
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SKILL_NAME = "anime-image-restyle"

# Files that ship inside the archive, relative to the repository root.
# Every entry is nested under a top-level <SKILL_NAME>/ folder so the archive
# unpacks as a single self-contained skill directory.
INCLUDE_FILES = [
    "SKILL.md",
    "README.md",
    "README_EN.md",
    "LICENSE",
    "references/style-registry.md",
    "references/prompt-lexicon.md",
    "scripts/probe_image.py",
]


def read_version(skill_md_path):
    """Parse the `version:` value from SKILL.md YAML frontmatter."""
    try:
        with open(skill_md_path, "r", encoding="utf-8") as f:
            head = f.read(2048)
    except OSError as exc:
        raise SystemExit("error: cannot read SKILL.md: %s" % exc)

    match = re.search(r"^version:\s*[\"']?([0-9][0-9A-Za-z.\-+]*)[\"']?\s*$",
                      head, re.MULTILINE)
    if not match:
        raise SystemExit("error: no `version:` field found in SKILL.md frontmatter")
    return match.group(1)


def build_archive(version, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    zip_name = "%s-v%s.zip" % (SKILL_NAME, version)
    zip_path = os.path.join(output_dir, zip_name)

    missing = [rel for rel in INCLUDE_FILES
               if not os.path.isfile(os.path.join(ROOT, rel))]
    if missing:
        raise SystemExit("error: missing expected files: %s" % ", ".join(missing))

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in INCLUDE_FILES:
            src = os.path.join(ROOT, rel)
            zf.write(src, "%s/%s" % (SKILL_NAME, rel.replace("\\", "/")))

    return zip_path


def verify_archive(zip_path):
    """Re-open the archive and confirm every expected member is present."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        if zf.testzip() is not None:
            raise SystemExit("error: corrupt entry detected in %s" % zip_path)
        members = set(zf.namelist())
        for rel in INCLUDE_FILES:
            expected = "%s/%s" % (SKILL_NAME, rel.replace("\\", "/"))
            if expected not in members:
                raise SystemExit("error: %s missing from archive" % expected)
        return len(members)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", help="override the version parsed from SKILL.md")
    parser.add_argument("--output-dir", default=os.path.join(ROOT, "dist"),
                        help="directory for the generated zip (default: <repo>/dist)")
    args = parser.parse_args()

    version = args.version or read_version(os.path.join(ROOT, "SKILL.md"))
    zip_path = build_archive(version, args.output_dir)
    count = verify_archive(zip_path)

    size_kb = os.path.getsize(zip_path) / 1024.0
    print("packed %d files -> %s (%.1f KB)" % (count, zip_path, size_kb))
    return 0


if __name__ == "__main__":
    sys.exit(main())
