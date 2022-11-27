"""
generators/model.py
Ian Kollipara
2022.11.26

Tortoise Model Generator
"""

# Imports
from os import curdir
from pathlib import Path
from tomllib import loads
from cstack._internal import templater

PROJECT = loads(Path("pyproject.toml").read_text("utf-8"))


class ModelGenerator:
    def __init__(self, model_name: str) -> None:
        self.model_path = (
            Path(curdir)
            / PROJECT["tool"]["poetry"]["name"]
            / Path("api")
            / "models"
            / f"{model_name.lower()}.py"
        )

    def __call__(self):
        self.model_path.write_text(
            templater.render(
                "api_model.py.j2",
                {"model_name": self.model_path.name.removesuffix(".py").title()},
            )
        )

        with (
            Path(curdir)
            / PROJECT["tool"]["poetry"]["name"]
            / Path("api")
            / "models"
            / "__init__.py"
        ).open("a") as f:
            f.write(
                f"from .{self.model_path.name.removesuffix('py').lower()} import {self.model_path.name.removesuffix('py').title()}"
            )
