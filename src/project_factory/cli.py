"""Command-line interface for AI Project Factory."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError as PydanticValidationError
from rich.console import Console
from rich.table import Table

from project_factory.config import ProjectConfig, ProjectType, feature_names
from project_factory.design import (
    AnimationPreference,
    ColorPalette,
    ThemeMode,
    TypographyPreset,
    UIStyle,
    design_for_generation,
    get_ui_style,
    ui_style_catalog,
)
from project_factory.generator import TEMPLATES, generate_project
from project_factory.validation import (
    ValidationError,
    parse_project_type,
    validate_project_name,
)

app = typer.Typer(
    name="project-factory",
    help="Generate lightweight, Codex-ready software project starters.",
    no_args_is_help=True,
)
console = Console()


def _abort(message: str) -> None:
    console.print(f"[red]Error:[/red] {message}", highlight=False)
    raise typer.Exit(code=2)


@app.command("list-templates")
def list_templates() -> None:
    """List available starter profiles."""

    table = Table(title="AI Project Factory templates")
    table.add_column("Type", style="cyan")
    table.add_column("Description")
    table.add_column("Optional features")
    for template in TEMPLATES:
        features = ", ".join(feature_names(template.project_type)) or "none"
        table.add_row(template.project_type.value, template.summary, features)
    console.print(table)


@app.command("list-ui-styles")
def list_ui_styles(
    details: Annotated[
        bool,
        typer.Option("--details", help="Show recommended uses, layout, and theme behavior."),
    ] = False,
) -> None:
    """List the visual design presets available to frontend projects."""

    if details:
        console.print("[bold]AI Project Factory UI styles[/bold]")
        for preset in ui_style_catalog():
            console.print(f"\n[cyan]{preset['id']}[/cyan] — [bold]{preset['name']}[/bold]")
            console.print(preset["description"], highlight=False)
            console.print(
                f"Recommended for: {', '.join(preset['recommended_for'])}", highlight=False
            )
            console.print(f"Default layout: {preset['default_layout']}", highlight=False)
            console.print(f"Theme behavior: {preset['theme_behavior']}", highlight=False)
        return

    table = Table(title="AI Project Factory UI styles")
    table.add_column("Identifier", style="cyan")
    table.add_column("Name")
    table.add_column("Description")
    for preset in ui_style_catalog():
        values = [preset["id"], preset["name"], preset["description"]]
        table.add_row(*values)
    console.print(table)


@app.command()
def create(
    name: Annotated[str | None, typer.Option(help="Kebab-case project name.")] = None,
    project_type: Annotated[
        str | None,
        typer.Option("--type", help="Starter profile: python-cli, web-saas, or ai-service."),
    ] = None,
    description: Annotated[
        str | None,
        typer.Option(help="Short project description."),
    ] = None,
    output: Annotated[
        Path | None,
        typer.Option(help="Exact destination path; it must not already exist."),
    ] = None,
    feature: Annotated[
        list[str] | None,
        typer.Option("--feature", help="Optional feature; repeat for multiple features."),
    ] = None,
    ui_style: Annotated[
        str | None,
        typer.Option("--ui-style", help="Visual preset for frontend projects."),
    ] = None,
    ui_layout: Annotated[
        str | None,
        typer.Option("--ui-layout", help="Page composition independent of visual style."),
    ] = None,
    theme: Annotated[
        str | None,
        typer.Option("--theme", help="Theme mode: light, dark, or system."),
    ] = None,
    color_palette: Annotated[
        str | None,
        typer.Option("--color-palette", help="Named color palette override."),
    ] = None,
    primary_color: Annotated[
        str | None,
        typer.Option("--primary-color", help="Custom primary color as six-digit hex."),
    ] = None,
    accent_color: Annotated[
        str | None,
        typer.Option("--accent-color", help="Custom accent color as six-digit hex."),
    ] = None,
    typography: Annotated[
        str | None,
        typer.Option("--typography", help="Typography preset for frontend projects."),
    ] = None,
    animation: Annotated[
        str | None,
        typer.Option("--animation", help="Animation preference: none, subtle, or kinetic."),
    ] = None,
    ui_effect: Annotated[
        list[str] | None,
        typer.Option("--ui-effect", help="Optional UI effect; repeat for multiple effects."),
    ] = None,
) -> None:
    """Create a project from a Copier template."""

    interactive = name is None and project_type is None and output is None
    chosen_name = name or typer.prompt("Project name")
    chosen_type = project_type or typer.prompt("Project type", default=ProjectType.PYTHON_CLI.value)
    chosen_description = description or (
        typer.prompt("Description", default=f"A {chosen_name} project")
        if interactive
        else f"A {chosen_name} project"
    )
    chosen_output = output or Path(chosen_name)

    try:
        validate_project_name(chosen_name)
        parsed_type = parse_project_type(chosen_type)
        if interactive and parsed_type is ProjectType.WEB_SAAS:
            ui_style = typer.prompt("UI style", default=UIStyle.MINIMALISM.value)
            default_layout = get_ui_style(UIStyle(ui_style))["default_layout"]
            ui_layout = typer.prompt("UI layout", default=default_layout)
            theme = typer.prompt("Theme", default=ThemeMode.SYSTEM.value)
            color_palette = typer.prompt("Color palette", default=ColorPalette.STYLE_DEFAULT.value)
            typography = typer.prompt("Typography", default=TypographyPreset.STYLE_DEFAULT.value)
            animation = typer.prompt("Animation", default=AnimationPreference.SUBTLE.value)

        design_requested = any(
            value is not None
            for value in (
                ui_style,
                ui_layout,
                theme,
                color_palette,
                primary_color,
                accent_color,
                typography,
                animation,
            )
        ) or bool(ui_effect)
        if design_requested and parsed_type is not ProjectType.WEB_SAAS:
            raise ValidationError(
                "UI design options are supported only by the web-saas profile; "
                f"{parsed_type.value} remains backend/terminal-only"
            )
        design = None
        if parsed_type is ProjectType.WEB_SAAS:
            design = design_for_generation(
                style=ui_style or UIStyle.MINIMALISM,
                layout=ui_layout,
                theme=theme or ThemeMode.SYSTEM,
                color_palette=color_palette or ColorPalette.STYLE_DEFAULT,
                primary_color=primary_color,
                accent_color=accent_color,
                typography=typography or TypographyPreset.STYLE_DEFAULT,
                animation=animation,
                effects=set(ui_effect) if ui_effect is not None else None,
            )
        config = ProjectConfig.for_generation(
            name=chosen_name,
            description=chosen_description,
            project_type=parsed_type,
            features=set(feature or []),
            design=design,
        )
        destination = generate_project(config, chosen_output)
    except (ValidationError, PydanticValidationError, ValueError, RuntimeError) as exc:
        _abort(str(exc))

    console.print(f"[green]Created[/green] {parsed_type.value} project at {destination}")
    console.print("Next: edit project.yaml and docs/PROJECT.md, then open the project in Codex.")


def main() -> None:
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
