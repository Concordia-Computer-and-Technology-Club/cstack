"""
generators/model.py
Ian Kollipara
2022.11.26

Tortoise Model Generator
"""

# Imports
from os import curdir
from pathlib import Path
from cstack._internal import templater


class ModelGenerator:
    def __init__(self, model_name: str) -> None:
        self.model_path = curdir / Path("api") / "models" / f"{model_name}.py"

    def __call__(self):
        self.model_path.write_text(
            templater.render(
                "api_model.py.j2",
                {"model_name": self.model_path.name.removesuffix(".py").title()},
            )
        )
