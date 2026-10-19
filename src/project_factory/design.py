"""Data-driven UI design configuration and preset catalog."""

from __future__ import annotations

import json
import re
from enum import StrEnum
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class UIStyle(StrEnum):
    """Stable identifiers for the supported visual design presets."""

    NEUMORPHISM = "neumorphism"
    GLASSMORPHISM = "glassmorphism"
    CLAYMORPHISM = "claymorphism"
    SKEUOMORPHISM = "skeuomorphism"
    FLAT_DESIGN = "flat-design"
    MATERIAL_DESIGN = "material-design"
    BRUTALISM = "brutalism"
    NEO_BRUTALISM = "neo-brutalism"
    MINIMALISM = "minimalism"
    MAXIMALISM = "maximalism"
    BENTO_GRID = "bento-grid"
    AURORA_UI = "aurora-ui"
    LIQUID_GLASS = "liquid-glass"
    SWISS_INTERNATIONAL = "swiss-international"
    EDITORIAL_UI = "editorial-ui"
    DARK_LUXE = "dark-luxe"
    CYBERPUNK = "cyberpunk"
    RETRO_Y2K = "retro-y2k"
    TERMINAL_UI = "terminal-ui"
    SPATIAL_3D = "spatial-3d"
    ORGANIC_UI = "organic-ui"
    KINETIC_UI = "kinetic-ui"


class UILayout(StrEnum):
    STANDARD = "standard"
    DASHBOARD = "dashboard"
    BENTO_GRID = "bento-grid"
    EDITORIAL = "editorial"
    LANDING_PAGE = "landing-page"
    SIDEBAR_APPLICATION = "sidebar-application"
    SPLIT_SCREEN = "split-screen"
    FULL_SCREEN = "full-screen"


class ThemeMode(StrEnum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class ColorPalette(StrEnum):
    STYLE_DEFAULT = "style-default"
    NEUTRAL = "neutral"
    INDIGO_CYAN = "indigo-cyan"
    OCEAN = "ocean"
    FOREST = "forest"
    SUNSET = "sunset"
    MONOCHROME = "monochrome"


class TypographyPreset(StrEnum):
    STYLE_DEFAULT = "style-default"
    SANS = "sans"
    SERIF = "serif"
    MONOSPACE = "monospace"
    DISPLAY = "display"


class TypographyScale(StrEnum):
    COMPACT = "compact"
    DEFAULT = "default"
    COMFORTABLE = "comfortable"
    DISPLAY = "display"


class SurfaceLevel(StrEnum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class BorderRadius(StrEnum):
    NONE = "none"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    FULL = "full"


class AnimationPreference(StrEnum):
    NONE = "none"
    SUBTLE = "subtle"
    KINETIC = "kinetic"


class UIEffect(StrEnum):
    NONE = "none"
    SUBTLE_TRANSITIONS = "subtle-transitions"
    AURORA_GRADIENTS = "aurora-gradients"
    GLASS_SURFACES = "glass-surfaces"
    KINETIC_ANIMATION = "kinetic-animation"
    SPATIAL_DEPTH = "spatial-depth"


STYLE_DEFAULT_EFFECTS: dict[UIStyle, frozenset[UIEffect]] = {
    UIStyle.GLASSMORPHISM: frozenset({UIEffect.GLASS_SURFACES}),
    UIStyle.AURORA_UI: frozenset({UIEffect.AURORA_GRADIENTS}),
    UIStyle.LIQUID_GLASS: frozenset({UIEffect.GLASS_SURFACES}),
    UIStyle.SPATIAL_3D: frozenset({UIEffect.SPATIAL_DEPTH}),
    UIStyle.KINETIC_UI: frozenset({UIEffect.KINETIC_ANIMATION}),
}


HEX_COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")
CSS_HEX_COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?$")
SEMANTIC_COLOR_TOKENS = frozenset(
    {
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
)
THEME_TOKEN_GROUPS = frozenset({"colors", "typography", "surface", "motion"})
CAPABILITY_FIELDS = frozenset(
    {"composition", "surface", "interaction", "responsive", "accessibility"}
)


class ThemeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mode: ThemeMode = ThemeMode.SYSTEM
    palette: ColorPalette = ColorPalette.STYLE_DEFAULT
    primary_color: str | None = None
    accent_color: str | None = None

    @field_validator("primary_color", "accent_color")
    @classmethod
    def validate_hex_color(cls, value: str | None) -> str | None:
        if value is not None and not HEX_COLOR_PATTERN.fullmatch(value):
            raise ValueError("color values must use six-digit hex notation, for example #6366F1")
        return value.upper() if value else value


class TypographyConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    preset: TypographyPreset = TypographyPreset.STYLE_DEFAULT
    heading: str | None = None
    body: str | None = None
    scale: TypographyScale = TypographyScale.DEFAULT

    @field_validator("heading", "body")
    @classmethod
    def validate_font_name(cls, value: str | None) -> str | None:
        if value is not None:
            normalized = value.strip()
            if not normalized or len(normalized) > 80:
                raise ValueError("font names must contain between 1 and 80 characters")
            return normalized
        return value


class SurfaceConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    border_radius: BorderRadius = BorderRadius.MEDIUM
    shadow_intensity: SurfaceLevel = SurfaceLevel.MEDIUM
    transparency: SurfaceLevel = SurfaceLevel.NONE
    blur_intensity: SurfaceLevel = SurfaceLevel.NONE


class EffectsConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    animation: AnimationPreference = AnimationPreference.SUBTLE
    enhancements: set[UIEffect] = Field(default_factory=set)

    @model_validator(mode="after")
    def validate_effects(self) -> Self:
        if UIEffect.NONE in self.enhancements and len(self.enhancements) > 1:
            raise ValueError("the 'none' effect cannot be combined with other effects")
        if (
            UIEffect.KINETIC_ANIMATION in self.enhancements
            and self.animation is not AnimationPreference.KINETIC
        ):
            raise ValueError("kinetic-animation requires the kinetic animation preference")
        return self

    def values(self) -> tuple[str, ...]:
        return tuple(sorted(effect.value for effect in self.enhancements))


class ResponsiveConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mobile: bool = True
    tablet: bool = True
    desktop: bool = True

    @model_validator(mode="after")
    def at_least_one_viewport(self) -> Self:
        if not (self.mobile or self.tablet or self.desktop):
            raise ValueError("at least one responsive viewport must be enabled")
        return self


class AccessibilityConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target: str = "WCAG-2.2-AA"
    reduced_motion: bool = True

    @field_validator("target")
    @classmethod
    def validate_target(cls, value: str) -> str:
        if value != "WCAG-2.2-AA":
            raise ValueError("the supported accessibility target is WCAG-2.2-AA")
        return value


class DesignConfig(BaseModel):
    """Frontend design settings kept separate from application behavior."""

    model_config = ConfigDict(extra="forbid")

    enabled: bool = True
    style: UIStyle = UIStyle.MINIMALISM
    layout: UILayout | None = None
    theme: ThemeConfig = Field(default_factory=ThemeConfig)
    typography: TypographyConfig = Field(default_factory=TypographyConfig)
    surfaces: SurfaceConfig = Field(default_factory=SurfaceConfig)
    effects: EffectsConfig = Field(default_factory=EffectsConfig)
    responsive: ResponsiveConfig = Field(default_factory=ResponsiveConfig)
    accessibility: AccessibilityConfig = Field(default_factory=AccessibilityConfig)

    @model_validator(mode="after")
    def validate_compatibility(self) -> Self:
        preset = get_ui_style(self.style)
        if self.layout is None:
            self.layout = UILayout(preset["default_layout"])

        if not self.enabled:
            return self

        inferred_effects = not self.effects.enhancements
        if inferred_effects:
            self.effects.enhancements = set(STYLE_DEFAULT_EFFECTS.get(self.style, frozenset()))
            if (
                UIEffect.KINETIC_ANIMATION in self.effects.enhancements
                and self.effects.animation is AnimationPreference.SUBTLE
            ):
                self.effects.animation = AnimationPreference.KINETIC
            if UIEffect.GLASS_SURFACES in self.effects.enhancements:
                self.surfaces.transparency = SurfaceLevel.MEDIUM
                self.surfaces.blur_intensity = SurfaceLevel.MEDIUM

        if (
            self.effects.animation is AnimationPreference.KINETIC
            and not self.accessibility.reduced_motion
        ):
            raise ValueError("kinetic animation requires reduced-motion alternatives")
        if self.style is UIStyle.KINETIC_UI and self.effects.animation is AnimationPreference.NONE:
            raise ValueError("kinetic-ui requires subtle or kinetic animation")
        if UIEffect.GLASS_SURFACES in self.effects.enhancements and (
            self.surfaces.transparency is SurfaceLevel.NONE
            or self.surfaces.blur_intensity is SurfaceLevel.NONE
        ):
            raise ValueError("glass-surfaces requires non-none transparency and blur intensity")
        return self


def _catalog_path() -> Path:
    relative = Path("templates/web-saas/template/frontend/design-system/presets.json")
    repository_path = Path(__file__).resolve().parents[2] / relative
    if repository_path.is_file():
        return repository_path
    packaged = resources.files("project_factory").joinpath(*relative.parts)
    path = Path(str(packaged))
    if not path.is_file():
        raise RuntimeError("Bundled UI design preset catalog is missing")
    return path


def _require_non_empty_text(value: Any, *, field: str, style_id: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(f"UI design preset '{style_id}' has invalid {field}")


def _validate_theme_tokens(theme: Any, *, mode: str, style_id: str) -> None:
    if not isinstance(theme, dict):
        raise RuntimeError(f"UI design preset '{style_id}' must define a {mode} token mapping")
    missing_groups = THEME_TOKEN_GROUPS - set(theme)
    if missing_groups:
        raise RuntimeError(
            f"UI design preset '{style_id}' {mode} theme is missing: "
            f"{', '.join(sorted(missing_groups))}"
        )
    colors = theme["colors"]
    if not isinstance(colors, dict):
        raise RuntimeError(f"UI design preset '{style_id}' {mode}.colors must be a mapping")
    missing_colors = SEMANTIC_COLOR_TOKENS - set(colors)
    if missing_colors:
        raise RuntimeError(
            f"UI design preset '{style_id}' {mode} theme is missing semantic colors: "
            f"{', '.join(sorted(missing_colors))}"
        )
    for token in SEMANTIC_COLOR_TOKENS:
        value = colors[token]
        if not isinstance(value, str) or not CSS_HEX_COLOR_PATTERN.fullmatch(value):
            raise RuntimeError(
                f"UI design preset '{style_id}' has invalid {mode}.{token} color '{value}'"
            )
    for group in THEME_TOKEN_GROUPS - {"colors"}:
        values = theme[group]
        if not isinstance(values, dict) or not values:
            raise RuntimeError(
                f"UI design preset '{style_id}' {mode}.{group} must be a non-empty mapping"
            )
        for token, value in values.items():
            _require_non_empty_text(value, field=f"{mode}.{group}.{token}", style_id=style_id)


@lru_cache(maxsize=1)
def _validated_ui_style_catalog() -> tuple[dict[str, Any], ...]:
    """Load and validate the canonical frontend preset catalog once."""

    try:
        raw = json.loads(_catalog_path().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not load UI design preset catalog: {exc}") from exc
    if not isinstance(raw, list):
        raise RuntimeError("UI design preset catalog must be a JSON list")
    expected = tuple(style.value for style in UIStyle)
    found = tuple(item.get("id") for item in raw if isinstance(item, dict))
    if found != expected or len(raw) != len(expected):
        raise RuntimeError(
            "UI design preset catalog must define every supported style exactly once "
            "in the canonical order"
        )
    required = {
        "id",
        "name",
        "description",
        "recommended_for",
        "default_layout",
        "theme_behavior",
        "capabilities",
        "light",
        "dark",
    }
    for item in raw:
        style_id = item.get("id", "unknown")
        missing = required - set(item)
        if missing:
            raise RuntimeError(
                f"UI design preset '{style_id}' is missing: {', '.join(sorted(missing))}"
            )
        for field in ("name", "description", "theme_behavior"):
            _require_non_empty_text(item[field], field=field, style_id=style_id)
        recommended_for = item["recommended_for"]
        if not isinstance(recommended_for, list) or not recommended_for:
            raise RuntimeError(
                f"UI design preset '{style_id}' recommended_for must be a non-empty list"
            )
        for index, recommendation in enumerate(recommended_for):
            _require_non_empty_text(
                recommendation,
                field=f"recommended_for[{index}]",
                style_id=style_id,
            )
        capabilities = item["capabilities"]
        if not isinstance(capabilities, dict):
            raise RuntimeError(f"UI design preset '{style_id}' capabilities must be a mapping")
        missing_capabilities = CAPABILITY_FIELDS - set(capabilities)
        if missing_capabilities:
            raise RuntimeError(
                f"UI design preset '{style_id}' is missing capabilities: "
                f"{', '.join(sorted(missing_capabilities))}"
            )
        for field in CAPABILITY_FIELDS:
            _require_non_empty_text(
                capabilities[field], field=f"capabilities.{field}", style_id=style_id
            )
        UILayout(item["default_layout"])
        _validate_theme_tokens(item["light"], mode="light", style_id=style_id)
        _validate_theme_tokens(item["dark"], mode="dark", style_id=style_id)
    return tuple(raw)


def ui_style_catalog() -> tuple[dict[str, Any], ...]:
    """Return detached preset mappings so callers cannot poison the shared catalog."""

    return tuple(json.loads(json.dumps(preset)) for preset in _validated_ui_style_catalog())


def get_ui_style(style: UIStyle | str) -> dict[str, Any]:
    """Return a detached preset mapping so callers cannot mutate the cached catalog."""

    style_id = UIStyle(style).value
    for preset in _validated_ui_style_catalog():
        if preset["id"] == style_id:
            return json.loads(json.dumps(preset))
    raise ValueError(f"Unsupported UI style: {style_id}")  # pragma: no cover


def design_for_generation(
    *,
    style: UIStyle | str = UIStyle.MINIMALISM,
    layout: UILayout | str | None = None,
    theme: ThemeMode | str = ThemeMode.SYSTEM,
    color_palette: ColorPalette | str = ColorPalette.STYLE_DEFAULT,
    primary_color: str | None = None,
    accent_color: str | None = None,
    typography: TypographyPreset | str = TypographyPreset.STYLE_DEFAULT,
    animation: AnimationPreference | str | None = None,
    effects: set[UIEffect | str] | None = None,
) -> DesignConfig:
    """Build design configuration from CLI-friendly scalar values."""

    selected_style = UIStyle(style)
    selected_effects = (
        set(STYLE_DEFAULT_EFFECTS.get(selected_style, frozenset()))
        if effects is None
        else {UIEffect(effect) for effect in effects}
    )
    uses_glass = UIEffect.GLASS_SURFACES in selected_effects
    selected_animation = (
        AnimationPreference.KINETIC
        if animation is None
        and (selected_style is UIStyle.KINETIC_UI or UIEffect.KINETIC_ANIMATION in selected_effects)
        else AnimationPreference(animation or AnimationPreference.SUBTLE)
    )
    return DesignConfig(
        style=selected_style,
        layout=UILayout(layout) if layout else None,
        theme=ThemeConfig(
            mode=ThemeMode(theme),
            palette=ColorPalette(color_palette),
            primary_color=primary_color,
            accent_color=accent_color,
        ),
        typography=TypographyConfig(preset=TypographyPreset(typography)),
        effects=EffectsConfig(
            animation=selected_animation,
            enhancements=selected_effects,
        ),
        surfaces=SurfaceConfig(
            transparency=SurfaceLevel.MEDIUM if uses_glass else SurfaceLevel.NONE,
            blur_intensity=SurfaceLevel.MEDIUM if uses_glass else SurfaceLevel.NONE,
        ),
    )
