# flasksecforge/cli.py

import os
import shutil
import sys
from pathlib import Path

template_name = "flask_api_boilerplate"


def create_project(target_dir: Path):
    """
    Copy the flask API boilerplate into a new directory named `target_dir`.
    """
    src = Path(__file__).parent / "templates" / template_name
    dst = target_dir.resolve()

    if dst.exists():
        print(f"Error: target directory '{dst.name}' already exists. Please choose a different project name.", file=sys.stderr)
        sys.exit(1)

    try:
        shutil.copytree(src, dst)
        print(f"Created new Flask API project in '{dst}'")
    except Exception as e:
        print(f"Failed to create project: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog="flasksecforge",
        description="Scaffold a Flask-secure boilerplate API into a new directory."
    )
    parser.add_argument(
        "name",
        help="Name of the new project directory to create"
    )
    args = parser.parse_args()

    target = Path(args.name)
    create_project(target)


if __name__ == "__main__":
    main()
