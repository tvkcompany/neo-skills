#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED = ("name", "description")
SKIP_DIRS = {".git", "node_modules"}
BLOCK_SCALAR = re.compile(r"^[>|][+\-]?\d*$")
NULL_VALUES = {"", "~", "null", "Null", "NULL"}


def skill_files(root: Path) -> list[Path]:
    files = []
    for path in root.rglob("SKILL.md"):
        if not path.is_file():
            continue
        if SKIP_DIRS.intersection(path.relative_to(root).parts):
            continue
        files.append(path)
    return sorted(files)


def frontmatter(text: str) -> str | None:
    if text.startswith("\ufeff"):
        text = text.removeprefix("\ufeff")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index])
    return None


def is_key(value: str) -> bool:
    if not value or not value[0].isalpha():
        return False
    return all(char.isalnum() or char in "-_" for char in value[1:])


def scalar(parts: list[str]) -> str | None:
    if not parts:
        return ""
    head = parts[0]
    tail = [part for part in parts[1:] if part]
    if BLOCK_SCALAR.fullmatch(head):
        return " ".join(tail).strip()
    if head.startswith(("-", "[", "{")):
        return None
    if len(head) >= 2 and head[0] == head[-1] and head[0] in "\"'":
        return head[1:-1].strip()
    if head in NULL_VALUES:
        return ""
    if tail:
        return " ".join([head, *tail]).strip()
    return head.strip()


def fields(body: str) -> dict[str, str | None] | None:
    parsed: dict[str, list[str]] = {}
    key: str | None = None
    for line in body.splitlines():
        if key is not None and (line.startswith(" ") or line.startswith("\t")):
            parsed[key].append(line.strip())
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line[:1].isspace():
            return None
        name, separator, value = line.partition(":")
        if separator == "" or not is_key(name):
            return None
        key = name
        parsed[key] = [value.strip()]
    return {name: scalar(parts) for name, parts in parsed.items()}


def problems(text: str) -> list[str]:
    body = frontmatter(text)
    if body is None:
        return ["missing frontmatter"]
    parsed = fields(body)
    if parsed is None:
        return ["invalid frontmatter"]
    found = []
    for name in REQUIRED:
        if name not in parsed or parsed[name] == "":
            found.append(f"missing {name}")
        elif parsed[name] is None:
            found.append(f"{name} is not text")
    return found


def check(root: Path) -> tuple[list[Path], list[tuple[Path, str]]]:
    files = skill_files(root)
    failures: list[tuple[Path, str]] = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            failures.append((path, "not valid UTF-8"))
            continue
        for problem in problems(text):
            failures.append((path, problem))
    return files, failures


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    files, failures = check(root)
    if not files:
        print("::error::No SKILL.md files found.")
        return 1
    for path, problem in failures:
        relative = path.relative_to(root).as_posix()
        print(f"::error file={relative}::{problem}")
    if failures:
        return 1
    print(f"Checked {len(files)} SKILL.md files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
