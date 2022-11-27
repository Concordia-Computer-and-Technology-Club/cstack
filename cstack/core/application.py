"""
core/application.py
Ian Kollipara
2022.11.25

Cstack Main Application Configuration
"""

# Imports
from pathlib import Path
from tomllib import loads
from fastapi import FastAPI
from .api import API
from .spa import SinglePageApplication

PROJECT = loads(Path("pyproject.toml").read_text("utf-8"))


def Application(*, api: API, view_dist: str = "view/dist"):
    api = api
    view = SinglePageApplication(
        directory=f"{PROJECT['tool']['poetry']['name']}/{view_dist}"
    )

    app = FastAPI()
    app.mount("/api", api.app, "api")
    app.mount("/", view, "view")
    return app
