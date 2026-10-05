from __future__ import annotations

import argparse
import json
from pathlib import Path

from .bundle import build
from .publish import promote, publish
from .reader import SkillReader
from .storage import configured_store


def main():
    parser = argparse.ArgumentParser(prog="fish-skills")
    commands = parser.add_subparsers(dest="command", required=True)
    cmd = commands.add_parser("build")
    cmd.add_argument("--root", type=Path, default=Path("."))
    cmd.add_argument("--output", type=Path, default=Path("dist"))
    cmd = commands.add_parser("publish")
    cmd.add_argument("archive", type=Path)
    cmd.add_argument("--activate", action="store_true")
    cmd = commands.add_parser("promote")
    cmd.add_argument("version")
    cmd.add_argument("--channel", choices=["preview", "stable"], required=True)
    cmd = commands.add_parser("read")
    cmd.add_argument("--channel", choices=["preview", "stable"], default="preview")
    cmd.add_argument("--version")
    cmd.add_argument("--skill")
    cmd.add_argument("--path")
    args = parser.parse_args()
    try:
        if args.command == "build":
            result = build(args.root, args.output)
        elif args.command == "publish":
            result = publish(configured_store(), args.archive, args.activate)
        elif args.command == "promote":
            result = promote(configured_store(), args.version, args.channel)
        else:
            reader = SkillReader(configured_store(), args.channel)
            if args.path:
                if not args.version:
                    raise ValueError("Reference reads require --version")
                result = reader.get_file(args.version, args.path)
            elif args.skill:
                result = reader.get_instructions(args.skill, args.version)
            else:
                result = reader.list_skills(args.version)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, FileNotFoundError, KeyError) as error:
        parser.exit(1, f"fish-skills: {error}\n")


if __name__ == "__main__":
    main()
