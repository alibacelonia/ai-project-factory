"""Validated configuration for generated projects."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from project_factory.design import DesignConfig


class ProjectType(StrEnum):
    """Supported starter profiles."""

    PYTHON_CLI = "python-cli"
    WEB_SAAS = "web-saas"
    AI_SERVICE = "ai-service"


PROFILE_FEATURES: dict[ProjectType, frozenset[str]] = {
    ProjectType.PYTHON_CLI: frozenset(),
    ProjectType.WEB_SAAS: frozenset(
        {
            "authentication",
            "database_migrations",
            "ai_integration",
            "background_jobs",
            "subscriptions",
            "email_notifications",
        }
    ),
    ProjectType.AI_SERVICE: frozenset(
        {
            "ai_integration",
            "background_jobs",
            "llm_provider",
            "aws_bedrock",
            "openai_api",
            "rag",
            "vector_database",
            "document_processing",
        }
    ),
}


class ProjectMetadata(BaseModel):
    name: str
    description: str
    type: ProjectType
    stage: str = "mvp"
    template_version: str = "0.2.0"


class StackConfig(BaseModel):
    language: str
    backend: str | None = None
    frontend: str | None = None
    database: str | None = None


class FeatureConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    authentication: bool = False
    database_migrations: bool = False
    ai_integration: bool = False
    background_jobs: bool = False
    subscriptions: bool = False
    email_notifications: bool = False
    llm_provider: bool = False
    aws_bedrock: bool = False
    openai_api: bool = False
    rag: bool = False
    vector_database: bool = False
    document_processing: bool = False

    def enabled(self) -> set[str]:
        return {name for name, value in self.model_dump().items() if value}


class DeploymentConfig(BaseModel):
    provider: str = "local"
    docker: bool = False


class DevelopmentConfig(BaseModel):
    testing: bool = True
    linting: bool = True
    ci_cd: bool = True


class ConstraintConfig(BaseModel):
    prioritize_low_cost: bool = True
    offline_development: bool = True


class ProjectConfig(BaseModel):
    """Canonical schema for every generated ``project.yaml``."""

    model_config = ConfigDict(extra="forbid")

    project: ProjectMetadata
    stack: StackConfig
    features: FeatureConfig = Field(default_factory=FeatureConfig)
    deployment: DeploymentConfig = Field(default_factory=DeploymentConfig)
    development: DevelopmentConfig = Field(default_factory=DevelopmentConfig)
    constraints: ConstraintConfig = Field(default_factory=ConstraintConfig)
    design: DesignConfig | None = None

    @model_validator(mode="after")
    def validate_profile_features(self) -> ProjectConfig:
        enabled = self.features.enabled()
        allowed = PROFILE_FEATURES[self.project.type]
        unsupported = enabled - allowed
        if unsupported:
            joined = ", ".join(sorted(unsupported))
            raise ValueError(f"{self.project.type.value} does not support: {joined}")

        if (
            self.features.aws_bedrock or self.features.openai_api
        ) and not self.features.llm_provider:
            raise ValueError("aws_bedrock and openai_api require llm_provider")
        if self.features.llm_provider and not self.features.ai_integration:
            raise ValueError("llm_provider requires ai_integration")
        if self.features.rag and not self.features.vector_database:
            raise ValueError("rag requires vector_database")
        if self.features.rag and not self.features.ai_integration:
            raise ValueError("rag requires ai_integration")
        if self.features.subscriptions and not self.features.authentication:
            raise ValueError("subscriptions requires authentication")
        if self.design is not None and self.project.type is not ProjectType.WEB_SAAS:
            raise ValueError(
                f"{self.project.type.value} does not include a graphical frontend; "
                "design is unsupported"
            )
        return self

    @classmethod
    def for_generation(
        cls,
        *,
        name: str,
        description: str,
        project_type: ProjectType,
        features: set[str] | None = None,
        design: DesignConfig | None = None,
    ) -> ProjectConfig:
        selected = features or set()
        unknown = selected - set(FeatureConfig.model_fields)
        if unknown:
            raise ValueError(f"Unknown features: {', '.join(sorted(unknown))}")
        feature_config = FeatureConfig(**{feature: True for feature in selected})
        stacks = {
            ProjectType.PYTHON_CLI: StackConfig(language="python"),
            ProjectType.WEB_SAAS: StackConfig(
                language="typescript/python",
                backend="fastapi",
                frontend="nextjs",
                database="postgresql",
            ),
            ProjectType.AI_SERVICE: StackConfig(language="python", backend="fastapi"),
        }
        return cls(
            project=ProjectMetadata(
                name=name,
                description=description,
                type=project_type,
            ),
            stack=stacks[project_type],
            features=feature_config,
            deployment=DeploymentConfig(docker=project_type is ProjectType.WEB_SAAS),
            design=design or (DesignConfig() if project_type is ProjectType.WEB_SAAS else None),
        )

    @classmethod
    def from_yaml(cls, path: Path) -> ProjectConfig:
        try:
            raw: Any = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            raise ValueError(f"Could not read configuration from {path}: {exc}") from exc
        if not isinstance(raw, dict):
            raise ValueError(f"Configuration in {path} must be a YAML mapping")
        return cls.model_validate(raw)


def feature_names(project_type: ProjectType) -> tuple[str, ...]:
    """Return supported feature names in a stable order."""

    return tuple(sorted(PROFILE_FEATURES[project_type]))
