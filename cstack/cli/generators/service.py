"""
generators/service.py
Ian Kollipara
2022.11.25

Service Generator
"""

# Imports
from os import curdir
from tomllib import loads
from typing import Literal
from cstack._internal import templater
from pathlib import Path

PROJECT = loads(Path("pyproject.toml").read_text("utf-8"))


class ServiceGenerator:
    def __init__(self, name: str, feature_name: str) -> None:
        self.service_name = (
            Path(curdir)
            / PROJECT["tool"]["poetry"]["name"]
            / Path("api")
            / feature_name
            / name
        )

    def __call__(self, type_: Literal["module", "class"]):
        match type_:
            case "module":
                self.service_name.write_text(
                    templater.render(
                        "service_module.py.j2",
                        {"service_name": self.service_name.name.title()},
                    )
                )
            case "class":
                self.service_name.write_text(
                    templater.render(
                        "service_class.py.j2",
                        {"service_name": self.service_name.name.title()},
                    )
                )
