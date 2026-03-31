#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install the bundled skill-auditor skill into the user's Codex skills directory."
    )
    parser.add_argument(
        "--dest-root",
        default=None,
        help="Override the skills root. Defaults to $CODEX_HOME/skills or ~/.codex/skills.",
    )
    parser.add_argument(
        "--name",
        default="skill-auditor",
        help="Installed skill directory name. Defaults to skill-auditor.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing installation at the target path.",
    )
    parser.add_argument(
        "--print-path",
        action="store_true",
        help="Print only the installed path on success.",
    )
    return parser.parse_args()


def default_dest_root() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return codex_home / "skills"


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    source = repo_root / "skill" / "skill-auditor"

    if not source.exists():
        print(f"Bundled skill source was not found: {source}", file=sys.stderr)
        return 1

    dest_root = Path(args.dest_root).expanduser() if args.dest_root else default_dest_root()
    target = dest_root / args.name

    dest_root.mkdir(parents=True, exist_ok=True)

    if target.exists():
        if not args.force:
            print(
                f"Target already exists: {target}\n"
                "Use --force to replace it.",
                file=sys.stderr,
            )
            return 1
        shutil.rmtree(target)

    shutil.copytree(source, target)

    if args.print_path:
        print(target)
        return 0

    print(f"Installed skill to: {target}")
    print("Restart Codex to pick up the new skill.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

