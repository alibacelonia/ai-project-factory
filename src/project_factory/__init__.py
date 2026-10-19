"""AI Project Factory package."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("ai-project-factory")
except PackageNotFoundError:  # pragma: no cover - source tree without installation
    __version__ = "0.2.0"

__all__ = ["__version__"]
