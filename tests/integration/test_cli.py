from pathlib import Path

import yaml
from typer.testing import CliRunner

from project_factory.cli import app
from project_factory.design import UIStyle

runner = CliRunner()


def test_list_templates() -> None:
    result = runner.invoke(app, ["list-templates"])

    assert result.exit_code == 0
    assert "python-cli" in result.stdout
    assert "web-saas" in result.stdout
    assert "ai-service" in result.stdout


def test_non_interactive_create(tmp_path: Path) -> None:
    target = tmp_path / "cli-example"
    result = runner.invoke(
        app,
        [
            "create",
            "--name",
            "cli-example",
            "--type",
            "python-cli",
            "--description",
            "CLI example",
            "--output",
            str(target),
        ],
    )

    assert result.exit_code == 0, result.stdout
    assert target.is_dir()


def test_unsupported_profile_has_controlled_error(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        [
            "create",
            "--name",
            "bad-profile",
            "--type",
            "mobile",
            "--output",
            str(tmp_path / "bad-profile"),
        ],
    )

    assert result.exit_code == 2
    assert "Unsupported project type" in result.stdout


def test_list_ui_styles_shows_all_stable_identifiers() -> None:
    result = runner.invoke(app, ["list-ui-styles"])

    assert result.exit_code == 0, result.stdout
    for style in UIStyle:
        assert style.value in result.stdout


def test_list_ui_styles_details_shows_design_guidance() -> None:
    result = runner.invoke(app, ["list-ui-styles", "--details"])

    assert result.exit_code == 0, result.stdout
    assert "Recommended for:" in result.stdout
    assert "Default layout:" in result.stdout
    assert "Theme behavior:" in result.stdout
    assert "premium" in result.stdout
    assert "dashboards" in result.stdout


def test_web_create_accepts_all_design_options(tmp_path: Path) -> None:
    target = tmp_path / "designed-web"
    result = runner.invoke(
        app,
        [
            "create",
            "--name",
            "designed-web",
            "--type",
            "web-saas",
            "--output",
            str(target),
            "--ui-style",
            "glassmorphism",
            "--ui-layout",
            "dashboard",
            "--theme",
            "dark",
            "--color-palette",
            "indigo-cyan",
            "--primary-color",
            "#6366f1",
            "--accent-color",
            "#22d3ee",
            "--typography",
            "sans",
            "--animation",
            "kinetic",
            "--ui-effect",
            "glass-surfaces",
            "--ui-effect",
            "kinetic-animation",
        ],
    )

    assert result.exit_code == 0, result.stdout
    project = yaml.safe_load((target / "project.yaml").read_text(encoding="utf-8"))
    assert project["design"]["style"] == "glassmorphism"
    assert project["design"]["layout"] == "dashboard"
    assert project["design"]["theme"] == {
        "mode": "dark",
        "palette": "indigo-cyan",
        "primary_color": "#6366F1",
        "accent_color": "#22D3EE",
    }
    assert project["design"]["typography"]["preset"] == "sans"
    assert project["design"]["effects"] == {
        "animation": "kinetic",
        "enhancements": ["glass-surfaces", "kinetic-animation"],
    }


def test_kinetic_style_uses_safe_motion_default(tmp_path: Path) -> None:
    target = tmp_path / "kinetic-web"
    result = runner.invoke(
        app,
        [
            "create",
            "--name",
            "kinetic-web",
            "--type",
            "web-saas",
            "--output",
            str(target),
            "--ui-style",
            "kinetic-ui",
        ],
    )

    assert result.exit_code == 0, result.stdout
    project = yaml.safe_load((target / "project.yaml").read_text(encoding="utf-8"))
    assert project["design"]["effects"]["animation"] == "kinetic"
    assert project["design"]["accessibility"]["reduced_motion"] is True


def test_invalid_design_option_has_controlled_error(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        [
            "create",
            "--name",
            "invalid-design",
            "--type",
            "web-saas",
            "--output",
            str(tmp_path / "invalid-design"),
            "--ui-style",
            "vaporwave",
        ],
    )

    assert result.exit_code == 2
    assert "vaporwave" in result.stdout


def test_ui_options_are_rejected_for_backend_only_profile(tmp_path: Path) -> None:
    target = tmp_path / "backend-design"
    result = runner.invoke(
        app,
        [
            "create",
            "--name",
            "backend-design",
            "--type",
            "ai-service",
            "--output",
            str(target),
            "--ui-style",
            "minimalism",
        ],
    )

    assert result.exit_code == 2
    assert "only by the web-saas profile" in result.stdout
    assert not target.exists()


def test_backend_only_create_has_no_design_section(tmp_path: Path) -> None:
    target = tmp_path / "plain-backend"
    result = runner.invoke(
        app,
        [
            "create",
            "--name",
            "plain-backend",
            "--type",
            "ai-service",
            "--output",
            str(target),
        ],
    )

    assert result.exit_code == 0, result.stdout
    project = yaml.safe_load((target / "project.yaml").read_text(encoding="utf-8"))
    assert "design" not in project


def test_interactive_web_create_prompts_for_design_choices(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(
        app,
        ["create"],
        input=(
            "interactive-web\n"
            "web-saas\n"
            "Interactive web project\n"
            "neo-brutalism\n"
            "landing-page\n"
            "light\n"
            "sunset\n"
            "display\n"
            "subtle\n"
        ),
    )

    assert result.exit_code == 0, result.stdout
    assert "UI style" in result.stdout
    project = yaml.safe_load(Path("interactive-web/project.yaml").read_text(encoding="utf-8"))
    assert project["design"]["style"] == "neo-brutalism"
    assert project["design"]["layout"] == "landing-page"


def test_interactive_backend_create_skips_design_prompts(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(
        app,
        ["create"],
        input="interactive-api\nai-service\nInteractive API\n",
    )

    assert result.exit_code == 0, result.stdout
    assert "UI style" not in result.stdout
    project = yaml.safe_load(Path("interactive-api/project.yaml").read_text(encoding="utf-8"))
    assert "design" not in project
