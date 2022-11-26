"""
core/application.py
Ian Kollipara
2022.11.25

Cstack Main Application Configuration
"""

# Imports
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api import API


class Application:
    def __init__(self, *, api: API, view_dist: str = "view/dist") -> None:
        self.api = api
        self.view = StaticFiles(directory=view_dist, html=True)

        app = FastAPI()
        app.mount("/api", self.api, "api")
        app.mount("/", self.view, "frontend")
        return app
