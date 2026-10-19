"""Input and destination validation."""

from __future__ import annotations

import keyword
import re
from pathlib import Path

from project_factory.config import ProjectType

PROJECT_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


class ValidationError(ValueError):
    """Raised when a generation request is unsafe or unsupported."""


def validate_project_name(name: str) -> str:
    if len(name) > 63 or not PROJECT_NAME_PATTERN.fullmatch(name):
        raise ValidationError(
            "Project name must be 1-63 characters of lowercase letters, numbers, and "
            "single hyphens, and must start with a letter."
        )
    if keyword.iskeyword(package_name(name)):
        raise ValidationError(
            f"Project name '{name}' is a reserved Python keyword. Choose another name."
        )
    return name


def parse_project_type(value: str) -> ProjectType:
    try:
        return ProjectType(value)
    except ValueError as exc:
        supported = ", ".join(item.value for item in ProjectType)
        raise ValidationError(
            f"Unsupported project type '{value}'. Choose from: {supported}"
        ) from exc


def validate_destination(destination: Path) -> Path:
    target = destination.expanduser().absolute()
    if target.exists() or target.is_symlink():
        raise ValidationError(f"Destination already exists: {target}")

    parent = target.parent
    existing_parent = parent
    while not existing_parent.exists() and existing_parent != existing_parent.parent:
        existing_parent = existing_parent.parent
    if not existing_parent.is_dir():
        raise ValidationError(f"Destination parent is not a directory: {existing_parent}")
    return target


def package_name(project_name: str) -> str:
    return project_name.replace("-", "_")
