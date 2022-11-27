"""
generators/feature.py
Ian Kollipara
2022.11.25

Feature Generation
"""

# Imports
from os import curdir
from pathlib import Path
from cstack._internal import templater
from tomllib import loads

PROJECT = loads(Path("pyproject.toml").read_text("utf-8"))


class FeatureGenerator:
    def __init__(self, feature_name: str) -> None:
        self.feature_path = (
            Path(curdir)
            / PROJECT["tool"]["poetry"]["name"]
            / Path("api")
            / "features"
            / feature_name
        )

    def create_router(self):
        (self.feature_path / "router.py").write_text(
            templater.render(
                "feature_router.py.j2", {"feature_name": self.feature_path.name.title()}
            )
        )

    def create_subdirectories(self):
        self.feature_path.mkdir()
        for directory in ("DTOs", "services", "repositories", "repositories/mock"):
            (self.feature_path / directory).mkdir()

    def create_feature_barrel(self):
        (self.feature_path / "__init__.py").write_text(
            templater.render(
                "feature_init.py.j2", {"feature_name": self.feature_path.name.title()}
            )
        )

    def create_test_file(self):
        (
            Path(curdir)
            / PROJECT["tool"]["poetry"]["name"]
            / Path("api")
            / "tests"
            / f"test_{self.feature_path.name.lower()}.py"
        ).write_text(
            templater.render(
                "feature_test.py.j2", {"feature_name": self.feature_path.name.title()}
            )
        )
