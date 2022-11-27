"""
Cstack CLI 
"""

# Imports
from pathlib import Path
from typer import Typer, Option
from rich.console import Console
from rich.prompt import Confirm
from enum import Enum
from cstack.cli.generators import ProjectGenerator
from cstack import __version__


app = Typer()
console = Console()


class NodeManagerChoices(str, Enum):
    NPM = "npm"
    YARN = "yarn"
    PNPM = "pnpm"


@app.command()
def new(
    project_name: str,
    dry_run: bool = Option(
        False, "--dry-run", help="Show output but don't create any files"
    ),
    no_vue: bool = Option(False, "--no-vue", help="Don't create frontend with Vue"),
    node_manager: NodeManagerChoices = Option(
        NodeManagerChoices.NPM, "--using", help="Which package manager to use."
    ),
):

    project = ProjectGenerator(project_name)

    if not dry_run:
        project.create_project_directory(not no_vue, node_manager.value)

    console.print(
        f":snake: [blue on white reverse] CREATED [/blue on white reverse] {project.proj_path.name.title()} Directory"
    )
    if not no_vue:
        console.print(
            f":computer: [blue on white reverse] CREATED [/blue on white reverse][green bold] Vue Frontend "
        )

    for directory in ("models", "features", "tests", "config"):
        if not dry_run:
            project.create_api_subdirectory(directory)
        console.print(
            f":sparkles: [blue on white reverse] CREATED [/blue on white reverse] Models Directory"
        )

    for file_config in (
        (Path("config") / "settings.py", "api_config_settings.py.j2", {}),
        (Path("config") / "env.py", "api_config_env.py.j2", {}),
        (
            Path("config") / "db.py",
            "api_config_db.py.j2",
            {"project_name": project.proj_path.name.title()},
        ),
        ("app.py", "api_app.py.j2", {"project_name": project.proj_path.name.title()}),
    ):
        if not dry_run:
            project.scaffold_api_file(*file_config)
        console.print(
            f":sparkles: [blue on white reverse] CREATED [/blue on white reverse] {file_config[0]}"
        )

    for file_config in (
        (".env", "env_file.j2", {}),
        (
            "pyproject.toml",
            "pyproject.toml",
            {"project_name": project.proj_path.name.lower(), "version": __version__},
        ),
        ("cstack", "cstack", {}),
    ):
        if not dry_run:
            project.scaffold_top_level_file(*file_config)
        console.print(
            f":sparkles: [blue on white reverse] CREATED [/blue on white reverse] {file_config[0]}"
        )

    if Confirm.ask(
        "Run [black on white reverse] Poetry Install [/black on white reverse]?"
    ):
        project.install()

    console.print(
        f":grey_exclamation: [bold blue] Creation Finished! [/bold blue]\nTo Continue type:\n`$ cd {project.proj_path.name}`"
    )
