from __future__ import annotations

import json
import os
import subprocess
import tomllib
from pathlib import Path

import pytest
import yaml

from project_factory.config import ProjectConfig, ProjectType
from project_factory.design import UIStyle, design_for_generation, ui_style_catalog
from project_factory.generator import generate_project
from project_factory.validation import ValidationError

REQUIRED_COMMON_FILES = {
    "AGENTS.md",
    ".codex/config.toml",
    ".codex/agents/software-architect.toml",
    ".codex/agents/security-reviewer.toml",
    "project.yaml",
    "docs/PROJECT.md",
    "docs/ARCHITECTURE.md",
    "docs/TASKS.md",
    "docs/DECISIONS.md",
    "docs/CHANGELOG.md",
    "README.md",
    ".env.example",
    ".gitignore",
    ".github/workflows/ci.yml",
    ".copier-answers.yml",
}
COMMON_SKILLS = {
    "project-bootstrap",
    "requirements-analysis",
    "feature-development",
    "testing",
    "code-review",
}
WEB_SKILLS = {"ui-design"}
COMMON_AGENTS = {"software-architect.toml", "security-reviewer.toml"}
WEB_AGENTS = {"ui-ux-engineer.toml"}


def make_config(project_type: ProjectType, name: str) -> ProjectConfig:
    return ProjectConfig.for_generation(
        name=name,
        description=f"Generated {project_type.value} test project",
        project_type=project_type,
    )


@pytest.mark.parametrize("project_type", list(ProjectType))
def test_generate_representative_project(tmp_path: Path, project_type: ProjectType) -> None:
    name = f"sample-{project_type.value}"
    target = tmp_path / name

    generated = generate_project(make_config(project_type, name), target)

    assert generated == target.absolute()
    assert {
        str(path.relative_to(target)) for path in target.rglob("*") if path.is_file()
    } >= REQUIRED_COMMON_FILES
    raw_config = yaml.safe_load((target / "project.yaml").read_text(encoding="utf-8"))
    assert raw_config["project"]["name"] == name
    assert raw_config["project"]["type"] == project_type.value
    ProjectConfig.model_validate(raw_config)
    assert name in (target / "README.md").read_text(encoding="utf-8")


def test_python_cli_substitutes_import_package(tmp_path: Path) -> None:
    target = tmp_path / "my-useful-cli"

    generate_project(make_config(ProjectType.PYTHON_CLI, "my-useful-cli"), target)

    assert (target / "src/my_useful_cli/cli.py").is_file()
    pyproject = tomllib.loads((target / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["name"] == "my-useful-cli"
    assert pyproject["project"]["scripts"]["my-useful-cli"] == "my_useful_cli.cli:app"


def test_existing_destination_is_not_modified(tmp_path: Path) -> None:
    target = tmp_path / "existing"
    target.mkdir()
    sentinel = target / "sentinel.txt"
    sentinel.write_text("preserve me", encoding="utf-8")

    with pytest.raises(ValidationError, match="already exists"):
        generate_project(make_config(ProjectType.PYTHON_CLI, "existing"), target)

    assert sentinel.read_text(encoding="utf-8") == "preserve me"
    assert list(target.iterdir()) == [sentinel]


@pytest.mark.parametrize("project_type", list(ProjectType))
def test_generated_skills_have_valid_metadata(tmp_path: Path, project_type: ProjectType) -> None:
    target = tmp_path / project_type.value
    generate_project(make_config(project_type, f"valid-{project_type.value}"), target)

    expected_skills = COMMON_SKILLS | (
        WEB_SKILLS if project_type is ProjectType.WEB_SAAS else set()
    )
    for skill in expected_skills:
        path = target / ".agents/skills" / skill / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        _, frontmatter, body = text.split("---", 2)
        metadata = yaml.safe_load(frontmatter)
        assert metadata["name"] == skill
        assert isinstance(metadata["description"], str)
        assert metadata["description"].strip()
        assert body.strip()


@pytest.mark.parametrize("project_type", list(ProjectType))
def test_generated_agent_toml_parses(tmp_path: Path, project_type: ProjectType) -> None:
    target = tmp_path / project_type.value
    generate_project(make_config(project_type, f"valid-{project_type.value}"), target)

    expected_agents = COMMON_AGENTS | (
        WEB_AGENTS if project_type is ProjectType.WEB_SAAS else set()
    )
    for filename in expected_agents:
        data = tomllib.loads((target / ".codex/agents" / filename).read_text(encoding="utf-8"))
        assert data["name"]
        assert data["description"]
        assert data["developer_instructions"]


@pytest.mark.parametrize(
    ("project_type", "relative_directory"),
    [
        (ProjectType.PYTHON_CLI, "."),
        (ProjectType.WEB_SAAS, "backend"),
        (ProjectType.AI_SERVICE, "."),
    ],
)
def test_generated_python_smoke_tests(
    tmp_path: Path, project_type: ProjectType, relative_directory: str
) -> None:
    target = tmp_path / project_type.value
    generate_project(make_config(project_type, f"smoke-{project_type.value}"), target)

    result = subprocess.run(
        ["uv", "run", "--extra", "dev", "pytest", "-q"],
        cwd=target / relative_directory,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
        env={**os.environ, "UV_NO_PROGRESS": "1"},
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_web_frontend_dependency_free_smoke(tmp_path: Path) -> None:
    target = tmp_path / "web"
    generate_project(make_config(ProjectType.WEB_SAAS, "smoke-web"), target)

    result = subprocess.run(
        ["npm", "test"],
        cwd=target / "frontend",
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_optional_features_change_only_selected_starter(tmp_path: Path) -> None:
    default_ai = tmp_path / "default-ai"
    external_ai = tmp_path / "external-ai"
    generate_project(make_config(ProjectType.AI_SERVICE, "default-ai"), default_ai)
    external_config = ProjectConfig.for_generation(
        name="external-ai",
        description="External adapter test",
        project_type=ProjectType.AI_SERVICE,
        features={
            "ai_integration",
            "llm_provider",
            "openai_api",
            "vector_database",
            "rag",
        },
    )
    generate_project(external_config, external_ai)

    assert '"openai' not in (default_ai / "pyproject.toml").read_text(encoding="utf-8")
    assert '"openai' in (external_ai / "pyproject.toml").read_text(encoding="utf-8")
    default_main = (default_ai / "src/default_ai/main.py").read_text(encoding="utf-8")
    external_main = (external_ai / "src/external_ai/main.py").read_text(encoding="utf-8")
    assert "/v1/rag" not in default_main
    assert "/v1/rag" in external_main

    auth_saas = tmp_path / "auth-saas"
    auth_config = ProjectConfig.for_generation(
        name="auth-saas",
        description="Authentication seam test",
        project_type=ProjectType.WEB_SAAS,
        features={"authentication"},
    )
    generate_project(auth_config, auth_saas)
    compose = (auth_saas / "docker-compose.yml").read_text(encoding="utf-8")
    assert "AUTH_DEVELOPMENT_TOKEN: ${AUTH_DEVELOPMENT_TOKEN:-}" in compose
    assert "127.0.0.1:5432:5432" in compose


def test_generation_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    config = make_config(ProjectType.PYTHON_CLI, "deterministic-cli")
    generate_project(config, first)
    generate_project(config, second)

    first_files = {
        str(path.relative_to(first)): path.read_bytes()
        for path in first.rglob("*")
        if path.is_file()
    }
    second_files = {
        str(path.relative_to(second)): path.read_bytes()
        for path in second.rglob("*")
        if path.is_file()
    }

    assert first_files == second_files


def test_description_is_safely_serialized(tmp_path: Path) -> None:
    target = tmp_path / "quoted-description"
    description = 'A "quoted" description\nwith a second line'
    config = ProjectConfig.for_generation(
        name="quoted-description",
        description=description,
        project_type=ProjectType.PYTHON_CLI,
    )

    generate_project(config, target)

    project_data = yaml.safe_load((target / "project.yaml").read_text(encoding="utf-8"))
    package_data = tomllib.loads((target / "pyproject.toml").read_text(encoding="utf-8"))
    assert project_data["project"]["description"] == description
    assert package_data["project"]["description"] == description

    web_target = tmp_path / "quoted-web"
    web_config = ProjectConfig.for_generation(
        name="quoted-web",
        description='JSX characters: <tag>{"value"}</tag>',
        project_type=ProjectType.WEB_SAAS,
    )
    generate_project(web_config, web_target)
    page = (web_target / "frontend/app/page.tsx").read_text(encoding="utf-8")
    assert r'{"JSX characters: \u003ctag\u003e{\"value\"}\u003c/tag\u003e"}' in page


def test_web_profile_generates_ui_skill_agent_and_references(tmp_path: Path) -> None:
    target = tmp_path / "designed-web"
    generate_project(make_config(ProjectType.WEB_SAAS, "designed-web"), target)

    references = target / ".agents/skills/ui-design/references"
    assert {path.stem for path in references.glob("*.md")} == {style.value for style in UIStyle}
    assert (target / ".codex/agents/ui-ux-engineer.toml").is_file()
    for project_type in (ProjectType.PYTHON_CLI, ProjectType.AI_SERVICE):
        backend_target = tmp_path / f"without-ui-{project_type.value}"
        generate_project(
            make_config(project_type, f"without-ui-{project_type.value}"), backend_target
        )
        assert not (backend_target / ".agents/skills/ui-design").exists()
        assert not (backend_target / ".codex/agents/ui-ux-engineer.toml").exists()
        raw = yaml.safe_load((backend_target / "project.yaml").read_text(encoding="utf-8"))
        assert "design" not in raw


@pytest.mark.parametrize("style", list(UIStyle))
def test_every_ui_style_generates_a_valid_project(tmp_path: Path, style: UIStyle) -> None:
    target = tmp_path / style.value
    config = ProjectConfig.for_generation(
        name=f"style-{style.value}",
        description=f"{style.value} showcase",
        project_type=ProjectType.WEB_SAAS,
        design=design_for_generation(style=style),
    )

    generate_project(config, target)

    project_data = yaml.safe_load((target / "project.yaml").read_text(encoding="utf-8"))
    assert project_data["design"]["style"] == style.value
    ProjectConfig.model_validate(project_data)
    generated_config = (target / "frontend/design-system/config.ts").read_text(encoding="utf-8")
    assert f'style: "{style.value}"' in generated_config
    css = (target / "frontend/app/styles.css").read_text(encoding="utf-8")
    assert f'[data-style="{style.value}"]' in css


def test_design_registry_tokens_css_and_gallery_stay_in_sync() -> None:
    catalog = list(ui_style_catalog())
    preset_path = Path("templates/web-saas/template/frontend/design-system/presets.json")
    css_path = Path("templates/web-saas/template/frontend/app/styles.css.jinja")
    gallery_app = Path("gallery/app.js")

    assert json.loads(preset_path.read_text(encoding="utf-8")) == catalog
    assert {preset["id"] for preset in catalog} == {style.value for style in UIStyle}
    semantic_colors = {
        "background",
        "foreground",
        "primary",
        "secondary",
        "accent",
        "surface",
        "muted",
        "destructive",
        "border",
        "focus",
    }
    for preset in catalog:
        for mode in ("light", "dark"):
            assert semantic_colors <= set(preset[mode]["colors"])
            assert preset[mode]["typography"]
            assert preset[mode]["surface"]
            assert preset[mode]["motion"]

    css = css_path.read_text(encoding="utf-8")
    for style in UIStyle:
        assert f'[data-style="{style.value}"]' in css
    assert ":focus-visible" in css
    assert "prefers-reduced-motion: reduce" in css
    assert "@supports not (backdrop-filter" in css
    assert gallery_app.is_file()
    assert "presets.json" in gallery_app.read_text(encoding="utf-8")


def test_style_switch_preserves_application_and_component_logic(tmp_path: Path) -> None:
    minimal = tmp_path / "minimal"
    cyber = tmp_path / "cyber"
    base = dict(
        name="switchable-ui",
        description="Safe style switch",
        project_type=ProjectType.WEB_SAAS,
        features={"authentication"},
    )
    generate_project(
        ProjectConfig.for_generation(
            **base, design=design_for_generation(style=UIStyle.MINIMALISM)
        ),
        minimal,
    )
    generate_project(
        ProjectConfig.for_generation(**base, design=design_for_generation(style=UIStyle.CYBERPUNK)),
        cyber,
    )

    for relative in (
        "backend/app/main.py",
        "backend/tests/test_health.py",
        "frontend/components/ui.tsx",
        "frontend/design-system/presets.json",
        "frontend/app/styles.css",
    ):
        assert (minimal / relative).read_bytes() == (cyber / relative).read_bytes()
    assert (minimal / "frontend/design-system/config.ts").read_bytes() != (
        cyber / "frontend/design-system/config.ts"
    ).read_bytes()
