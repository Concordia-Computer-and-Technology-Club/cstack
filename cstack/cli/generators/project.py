"""
generators/project.py
Ian Kollipara
2022.11.25

Project Generator
"""

# Imports
from pathlib import Path
from os import system, chdir, curdir, getcwd
from typing import Any, Literal
from cstack._internal import templater


class ProjectGenerator:
    def __init__(self, project_name: str) -> None:
        self.home_path = Path(project_name)
        self.proj_path = Path(project_name) / Path(
            project_name.replace(" ", "_").replace("-", "_").lower()
        )

    def create_project_directory(
        self, use_vue: bool = True, node_manager: Literal["npm", "yarn", "pnpm"] = "npm"
    ):
        self.home_path.mkdir()
        self.proj_path.mkdir()
        (self.proj_path / "api").mkdir()
        (self.proj_path / "__init__.py").write_text(
            templater.render(
                "__init__.py.j2", {"project_name": self.proj_path.name.title()}
            )
        )
        if use_vue:
            match node_manager:
                case "npm":
                    system(f"npm create vue@3 {self.proj_path}/view")
                case "yarn":
                    system(f"yarn create vue {self.proj_path}/view")
                case "pnpm":
                    system(f"pnpm create vue {self.proj_path}/view")

    def create_api_subdirectory(self, dirname: str):
        (self.proj_path / "api" / dirname).mkdir()

    def scaffold_api_file(
        self, filename: str, template: str, template_args: dict[str, Any]
    ):
        (self.proj_path / "api" / f"{filename}").write_text(
            templater.render(template, template_args)
        )

    def scaffold_top_level_file(
        self, filename: str, template: str, template_args: dict[str, Any]
    ):
        (self.home_path / f"{filename}").write_text(
            templater.render(template, template_args)
        )

    def install(self):
        chdir(self.home_path.relative_to(curdir))
        system("poetry install")
