from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from project_factory.config import ProjectConfig, ProjectType, feature_names
from project_factory.design import (
    AnimationPreference,
    DesignConfig,
    SurfaceLevel,
    UIEffect,
    UILayout,
    UIStyle,
    design_for_generation,
    get_ui_style,
    ui_style_catalog,
)
from project_factory.generator import _copier_data

EXPECTED_UI_STYLES = (
    "neumorphism",
    "glassmorphism",
    "claymorphism",
    "skeuomorphism",
    "flat-design",
    "material-design",
    "brutalism",
    "neo-brutalism",
    "minimalism",
    "maximalism",
    "bento-grid",
    "aurora-ui",
    "liquid-glass",
    "swiss-international",
    "editorial-ui",
    "dark-luxe",
    "cyberpunk",
    "retro-y2k",
    "terminal-ui",
    "spatial-3d",
    "organic-ui",
    "kinetic-ui",
)


def test_python_cli_configuration_defaults() -> None:
    config = ProjectConfig.for_generation(
        name="sample-cli",
        description="Sample",
        project_type=ProjectType.PYTHON_CLI,
    )

    assert config.stack.language == "python"
    assert config.features.enabled() == set()
    assert config.deployment.docker is False
    assert config.design is None
    assert config.project.template_version == "0.2.0"


def test_web_configuration_has_backward_compatible_design_defaults() -> None:
    config = ProjectConfig.for_generation(
        name="sample-web",
        description="Sample",
        project_type=ProjectType.WEB_SAAS,
    )

    assert config.design is not None
    assert config.design.style is UIStyle.MINIMALISM
    assert config.design.layout is UILayout.STANDARD
    assert config.design.theme.mode.value == "system"
    assert config.design.accessibility.reduced_motion is True


def test_profile_specific_feature_is_rejected() -> None:
    with pytest.raises(ValidationError, match="python-cli does not support"):
        ProjectConfig.for_generation(
            name="sample-cli",
            description="Sample",
            project_type=ProjectType.PYTHON_CLI,
            features={"authentication"},
        )


def test_provider_requires_ai_integration() -> None:
    with pytest.raises(ValidationError, match="llm_provider requires ai_integration"):
        ProjectConfig.for_generation(
            name="sample-ai",
            description="Sample",
            project_type=ProjectType.AI_SERVICE,
            features={"llm_provider"},
        )


def test_external_provider_requires_provider_abstraction() -> None:
    with pytest.raises(ValidationError, match="require llm_provider"):
        ProjectConfig.for_generation(
            name="sample-ai",
            description="Sample",
            project_type=ProjectType.AI_SERVICE,
            features={"ai_integration", "openai_api"},
        )


def test_rag_requires_vector_database() -> None:
    with pytest.raises(ValidationError, match="rag requires vector_database"):
        ProjectConfig.for_generation(
            name="sample-ai",
            description="Sample",
            project_type=ProjectType.AI_SERVICE,
            features={"ai_integration", "rag"},
        )


def test_rag_requires_ai_integration() -> None:
    with pytest.raises(ValidationError, match="rag requires ai_integration"):
        ProjectConfig.for_generation(
            name="sample-ai",
            description="Sample",
            project_type=ProjectType.AI_SERVICE,
            features={"rag", "vector_database"},
        )


def test_subscriptions_require_authentication() -> None:
    with pytest.raises(ValidationError, match="subscriptions requires authentication"):
        ProjectConfig.for_generation(
            name="sample-web",
            description="Sample",
            project_type=ProjectType.WEB_SAAS,
            features={"subscriptions"},
        )


def test_yaml_loader_validates_schema(tmp_path: Path) -> None:
    config = ProjectConfig.for_generation(
        name="sample-ai",
        description="Sample",
        project_type=ProjectType.AI_SERVICE,
    )
    path = tmp_path / "project.yaml"
    path.write_text(yaml.safe_dump(config.model_dump(mode="json")), encoding="utf-8")

    loaded = ProjectConfig.from_yaml(path)

    assert loaded == config


def test_legacy_web_yaml_without_design_remains_valid(tmp_path: Path) -> None:
    config = ProjectConfig.for_generation(
        name="sample-web",
        description="Sample",
        project_type=ProjectType.WEB_SAAS,
    ).model_dump(mode="json")
    config.pop("design")
    path = tmp_path / "project.yaml"
    path.write_text(yaml.safe_dump(config), encoding="utf-8")

    loaded = ProjectConfig.from_yaml(path)

    assert loaded.design is None


def test_feature_names_are_stable() -> None:
    names = feature_names(ProjectType.WEB_SAAS)
    assert names == tuple(sorted(names))
    assert "authentication" in names


def test_all_22_ui_style_identifiers_are_stable_and_loadable() -> None:
    assert tuple(style.value for style in UIStyle) == EXPECTED_UI_STYLES
    assert tuple(preset["id"] for preset in ui_style_catalog()) == EXPECTED_UI_STYLES

    for style_id in EXPECTED_UI_STYLES:
        assert get_ui_style(style_id)["id"] == style_id


def test_all_presets_define_semantic_tokens_for_both_themes() -> None:
    required_colors = {
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

    for preset in ui_style_catalog():
        for mode in ("light", "dark"):
            assert required_colors <= set(preset[mode]["colors"]), (preset["id"], mode)
            assert {"typography", "surface", "motion"} <= set(preset[mode])


def test_catalog_supports_css_alpha_hex_without_relaxing_user_colors() -> None:
    assert get_ui_style("glassmorphism")["light"]["colors"]["surface"] == "#FFFFFFB8"

    with pytest.raises(ValidationError, match="six-digit hex"):
        design_for_generation(primary_color="#6366F1CC")


def test_catalog_results_are_detached_from_the_cached_source() -> None:
    catalog = ui_style_catalog()
    catalog[0]["name"] = "Changed"

    assert ui_style_catalog()[0]["name"] == "Neumorphism"
    assert get_ui_style("neumorphism")["name"] == "Neumorphism"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("style", "vaporwave"),
        ("layout", "three-column-chaos"),
        ("theme", "sepia"),
        ("color_palette", "rainbow"),
        ("typography", "comic"),
        ("animation", "constant"),
    ],
)
def test_design_builder_rejects_unsupported_values(field: str, value: str) -> None:
    arguments = {field: value}

    with pytest.raises(ValueError):
        design_for_generation(**arguments)


@pytest.mark.parametrize("field", ["primary_color", "accent_color"])
@pytest.mark.parametrize("value", ["6366F1", "#FFF", "#GGGGGG", "rgb(1,2,3)"])
def test_design_rejects_invalid_colors(field: str, value: str) -> None:
    with pytest.raises(ValidationError, match="six-digit hex"):
        design_for_generation(**{field: value})


def test_design_normalizes_valid_colors() -> None:
    design = design_for_generation(primary_color="#abcdef", accent_color="#0123ab")

    assert design.theme.primary_color == "#ABCDEF"
    assert design.theme.accent_color == "#0123AB"


def test_none_effect_cannot_be_combined() -> None:
    with pytest.raises(ValidationError, match="cannot be combined"):
        design_for_generation(effects={UIEffect.NONE, UIEffect.AURORA_GRADIENTS})


def test_glass_effect_has_safe_transparency_and_blur_defaults() -> None:
    design = design_for_generation(effects={UIEffect.GLASS_SURFACES})

    assert design.surfaces.transparency is SurfaceLevel.MEDIUM
    assert design.surfaces.blur_intensity is SurfaceLevel.MEDIUM


@pytest.mark.parametrize(
    ("style", "expected_effect"),
    [
        ("glassmorphism", "glass-surfaces"),
        ("liquid-glass", "glass-surfaces"),
        ("aurora-ui", "aurora-gradients"),
        ("spatial-3d", "spatial-depth"),
        ("kinetic-ui", "kinetic-animation"),
    ],
)
def test_composition_and_motion_styles_infer_reusable_effects(
    style: str, expected_effect: str
) -> None:
    design = DesignConfig(style=style)

    assert expected_effect in design.effects.values()


@pytest.mark.parametrize(
    "style",
    ["glassmorphism", "liquid-glass", "aurora-ui", "spatial-3d", "kinetic-ui"],
)
def test_explicit_none_suppresses_inferred_style_effects(style: str) -> None:
    design = design_for_generation(style=style, effects={UIEffect.NONE})

    assert design.effects.values() == ("none",)


def test_glass_effect_rejects_missing_readability_surfaces() -> None:
    with pytest.raises(ValidationError, match="non-none transparency and blur"):
        DesignConfig(effects={"enhancements": ["glass-surfaces"]})


def test_kinetic_style_uses_motion_safe_default() -> None:
    design = design_for_generation(style=UIStyle.KINETIC_UI)

    assert design.effects.animation is AnimationPreference.KINETIC
    assert design.effects.values() == ("kinetic-animation",)
    assert design.accessibility.reduced_motion is True


def test_kinetic_style_rejects_disabled_animation() -> None:
    with pytest.raises(ValidationError, match="kinetic-ui requires"):
        DesignConfig(style="kinetic-ui", effects={"animation": "none"})


def test_kinetic_effect_requires_matching_preference() -> None:
    with pytest.raises(ValidationError, match="kinetic animation preference"):
        DesignConfig(
            effects={
                "animation": "subtle",
                "enhancements": ["kinetic-animation"],
            }
        )


def test_kinetic_animation_requires_reduced_motion_fallback() -> None:
    with pytest.raises(ValidationError, match="reduced-motion"):
        DesignConfig(
            effects={"animation": "kinetic"},
            accessibility={"reduced_motion": False},
        )


def test_explicit_design_is_rejected_for_backend_only_profiles() -> None:
    with pytest.raises(ValidationError, match="does not include a graphical frontend"):
        ProjectConfig.for_generation(
            name="sample-ai",
            description="Sample",
            project_type=ProjectType.AI_SERVICE,
            design=DesignConfig(),
        )


def test_disabled_design_is_still_rejected_for_backend_only_profiles() -> None:
    with pytest.raises(ValidationError, match="does not include a graphical frontend"):
        ProjectConfig.for_generation(
            name="sample-ai",
            description="Sample",
            project_type=ProjectType.AI_SERVICE,
            design=DesignConfig(enabled=False),
        )


def test_copier_design_data_is_deterministic() -> None:
    design = design_for_generation(effects={UIEffect.SPATIAL_DEPTH, UIEffect.AURORA_GRADIENTS})
    config = ProjectConfig.for_generation(
        name="sample-web",
        description="Sample",
        project_type=ProjectType.WEB_SAAS,
        design=design,
    )

    first = _copier_data(config)
    second = _copier_data(config)

    assert first == second
    assert first["ui_effects"] == ["aurora-gradients", "spatial-depth"]
    assert first["design_config"]["effects"]["enhancements"] == [
        "aurora-gradients",
        "spatial-depth",
    ]
