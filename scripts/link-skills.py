#!/usr/bin/env python3
"""Create and validate assistant adapters for the repository's canonical skills."""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ADAPTERS = (Path('.claude/skills'), Path('.codex/skills'), Path('.github/skills'))


def find_root() -> Path:
    for candidate in (Path(__file__).resolve().parent.parent, *Path(__file__).resolve().parents):
        if (candidate / 'skills').is_dir():
            return candidate
    raise RuntimeError('Could not find repository root containing skills/.')


def canonical_skills(root: Path) -> list[Path]:
    return sorted(p for p in (root / 'skills').iterdir() if p.is_dir() and (p / 'SKILL.md').is_file())


def is_link(path: Path) -> bool:
    if path.is_symlink():
        return True
    # pathlib does not expose junction detection on every supported Python
    # version. A junction resolves to a different absolute path than its
    # directory entry, while a normal directory resolves to itself.
    return platform.system() == 'Windows' and path.is_dir() and path.resolve() != path.absolute()


def remove_link(path: Path) -> None:
    if platform.system() == 'Windows' and path.is_dir() and not path.is_symlink():
        path.rmdir()
    else:
        path.unlink()


def make_link(link: Path, target: Path) -> str:
    relative_target = os.path.relpath(target, link.parent)
    if platform.system() != 'Windows':
        link.symlink_to(relative_target, target_is_directory=True)
        return 'symlink'
    try:
        link.symlink_to(relative_target, target_is_directory=True)
        return 'symlink'
    except OSError:
        subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(target)], check=True,
                       stdout=subprocess.DEVNULL)
        return 'junction'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='only validate existing adapters')
    args = parser.parse_args()
    root = find_root()
    skills = canonical_skills(root)
    if not skills:
        raise RuntimeError('No canonical skills found under skills/.')
    failures: list[str] = []
    for adapter in ADAPTERS:
        directory = root / adapter
        directory.mkdir(parents=True, exist_ok=True)
        for skill in skills:
            link = directory / skill.name
            target = root / 'skills' / skill.name
            if link.exists() or link.is_symlink():
                if not is_link(link):
                    failures.append(f'{link} exists and is not a link')
                    continue
                if link.resolve() != target.resolve():
                    if args.check:
                        failures.append(f'{link} points to {link.resolve()}, expected {target}')
                        continue
                    remove_link(link)
            if not args.check and not link.exists():
                print(f'{make_link(link, target)}: {link} -> {target}')
            if not link.exists() or link.resolve() != target.resolve():
                failures.append(f'{link} does not resolve to {target}')
    if failures:
        for failure in failures:
            print(f'ERROR: {failure}', file=sys.stderr)
        return 1
    print(f'Validated {len(skills)} canonical skills across {len(ADAPTERS)} adapters.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
