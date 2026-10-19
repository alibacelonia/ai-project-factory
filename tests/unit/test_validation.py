from pathlib import Path

import pytest

from project_factory.config import ProjectType
from project_factory.validation import (
    ValidationError,
    package_name,
    parse_project_type,
    validate_destination,
    validate_project_name,
)


@pytest.mark.parametrize("name", ["demo", "my-cli", "app2", "a-b-c"])
def test_valid_project_names(name: str) -> None:
    assert validate_project_name(name) == name


@pytest.mark.parametrize(
    "name",
    ["", "Upper", "with space", "-leading", "trailing-", "two--hyphens", "../escape", "1app"],
)
def test_invalid_project_names(name: str) -> None:
    with pytest.raises(ValidationError, match="Project name must"):
        validate_project_name(name)


@pytest.mark.parametrize("name", ["class", "async"])
def test_python_keyword_project_names_are_rejected(name: str) -> None:
    with pytest.raises(ValidationError, match="reserved Python keyword"):
        validate_project_name(name)


def test_parse_project_type_rejects_unsupported_profile() -> None:
    with pytest.raises(ValidationError, match="Unsupported project type"):
        parse_project_type("mobile-app")


def test_parse_project_type() -> None:
    assert parse_project_type("python-cli") is ProjectType.PYTHON_CLI


def test_existing_destination_is_rejected(tmp_path: Path) -> None:
    target = tmp_path / "existing"
    target.mkdir()
    sentinel = target / "keep.txt"
    sentinel.write_text("untouched", encoding="utf-8")

    with pytest.raises(ValidationError, match="already exists"):
        validate_destination(target)

    assert sentinel.read_text(encoding="utf-8") == "untouched"


def test_package_name_normalizes_hyphens() -> None:
    assert package_name("my-cli") == "my_cli"
