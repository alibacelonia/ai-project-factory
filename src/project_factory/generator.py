"""Copier-backed project generation."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any

from copier import run_copy

from project_factory.config import FeatureConfig, ProjectConfig, ProjectType
from project_factory.design import get_ui_style, ui_style_catalog
from project_factory.validation import package_name, validate_destination, validate_project_name


@dataclass(frozen=True)
class TemplateInfo:
    project_type: ProjectType
    summary: str


TEMPLATES = (
    TemplateInfo(ProjectType.PYTHON_CLI, "Typer/Rich Python CLI with tests and structured logs"),
    TemplateInfo(ProjectType.WEB_SAAS, "Next.js + FastAPI + PostgreSQL local starter"),
    TemplateInfo(ProjectType.AI_SERVICE, "FastAPI AI service with a local mock provider"),
)


def _template_path(project_type: ProjectType) -> Path:
    repository_path = Path(__file__).resolve().parents[2] / "templates" / project_type.value
    if repository_path.is_dir():
        return repository_path
    packaged = resources.files("project_factory").joinpath("templates", project_type.value)
    path = Path(str(packaged))
    if not path.is_dir():
        raise RuntimeError(f"Bundled template is missing: {project_type.value}")
    return path


def _copier_data(config: ProjectConfig) -> dict[str, Any]:
    feature_values = FeatureConfig().model_dump()
    feature_values.update(config.features.model_dump())
    data: dict[str, Any] = {
        "project_name": config.project.name,
        "project_slug": config.project.name,
        "package_name": package_name(config.project.name),
        "description": config.project.description,
        "project_type": config.project.type.value,
        "template_version": config.project.template_version,
        **feature_values,
    }
    if config.design is not None:
        design_config = config.design.model_dump(mode="json")
        design_config["effects"]["enhancements"] = list(config.design.effects.values())
        data.update(
            {
                "design_enabled": config.design.enabled,
                "ui_style": config.design.style.value,
                "ui_layout": config.design.layout.value,
                "theme_mode": config.design.theme.mode.value,
                "color_palette": config.design.theme.palette.value,
                # Copier string questions reject ``None`` even in default mode. The
                # templates convert these empty optional overrides back to YAML null.
                "primary_color": config.design.theme.primary_color or "",
                "accent_color": config.design.theme.accent_color or "",
                "typography_preset": config.design.typography.preset.value,
                "animation": config.design.effects.animation.value,
                "ui_effects": list(config.design.effects.values()),
                "design_config": design_config,
                "design_preset": get_ui_style(config.design.style),
                "design_catalog": list(ui_style_catalog()),
            }
        )
    return data


def generate_project(config: ProjectConfig, destination: Path) -> Path:
    """Generate atomically into a destination that must not already exist."""

    validate_project_name(config.project.name)
    target = validate_destination(destination)
    target.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=".project-factory-", dir=target.parent) as temporary:
        staging = Path(temporary) / target.name
        run_copy(
            src_path=str(_template_path(config.project.type)),
            dst_path=str(staging),
            data=_copier_data(config),
            defaults=True,
            overwrite=False,
            unsafe=False,
            quiet=True,
        )
        staging.replace(target)
    return target
