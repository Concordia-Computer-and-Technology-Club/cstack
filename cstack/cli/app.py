"""
Cstack CLI 
"""

# Imports
from pathlib import Path
from typer import Typer, Option
from rich.console import Console
from enum import Enum
from cstack.cli.generators import (
    ProjectGenerator,
    FeatureGenerator,
    ServiceGenerator,
    ModelGenerator,
)


app = Typer()
generate = Typer()
console = Console()


class NodeManagerChoices(str, Enum):
    NPM = "npm"
    YARN = "yarn"
    PNPM = "pnpm"


class ServiceTypes(str, Enum):
    CLASS = "class"
    MODULE = "module"


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

    project = ProjectGenerator(project_name.replace(" ", "_").replace("-", "_").lower())

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
            project.create_file(*file_config)
        console.print(
            f":sparkles: [blue on white reverse] CREATED [/blue on white reverse] {file_config[0]}"
        )

    for file_config in (
        (".env", "env_file.j2", {}),
        (
            "__init__.py",
            "__init__.py.j2",
            {"project_name": project.proj_path.name.title()},
        ),
        ("makefile", "makefile", {"project_name": project.proj_path.name.title()}),
        ("requirements.txt", "requirements.txt", {}),
    ):
        if not dry_run:
            project.create_base_file(*file_config)
        console.print(
            f":sparkles: [blue on white reverse] CREATED [/blue on white reverse] {file_config[0]}"
        )

    console.print(
        f":grey_exclamation: [bold blue] Creation Finished! [/bold blue]\nTo Continue type:\n`$ cd {project.proj_path.name}`"
    )


@generate.command("feature")
def gen_feature(
    name: str,
    without_test: bool = Option(
        False, "--without-test", help="Do not generate a test file"
    ),
    dry_run: bool = Option(False, "--dry-run", help="show output but don't generate"),
):

    feature = FeatureGenerator(name)

    if not dry_run:
        feature.create_subdirectories()
    console.log(
        f":sparkles: [blue on white reverse] Created [/blue on white reverse] {name.lower()}/ and subdirectories"
    )

    if not dry_run:
        feature.create_router()
    console.log(
        f":sparkles: [blue on white reverse] Created [/blue on white reverse] {name.lower()}/router.py"
    )

    if not dry_run:
        feature.create_feature_barrel()
    console.log(
        f":sparkles: [blue on white reverse] Created [/blue on white reverse] {name.lower()}/__init__.py"
    )

    if not without_test:
        if not dry_run:
            feature.create_test_file()
        console.log(
            f":sparkles: [blue on white reverse] Created [/blue on white reverse] tests/test_{name.lower()}.py"
        )


@generate.command("service")
def gen_service(
    name: str,
    feature: str,
    dry_run: bool = Option(False, "--dry-run", help="show output but don't generate"),
    type_: ServiceTypes = Option(
        ServiceTypes.MODULE, "-t", "--type", help="Type of Service to Generate"
    ),
):
    service = ServiceGenerator(name, feature)
    if not dry_run:
        service(type_.value)
    console.log(
        f":sparkles: [blue on white reverse] Created [/blue on white reverse] {feature.lower()}/services/{name.lower()}.py"
    )


@generate.command("model")
def gen_model(
    name: str,
    dry_run: bool = Option(False, "--dry-run", help="Show Output but don't generate"),
):
    model = ModelGenerator(name)

    if not dry_run:
        model()
    console.log(
        f":sparkles: [blue on white reverse] Created [/blue on white reverse] models/{name.lower()}.py"
    )


app.add_typer(generate, name="generate")
