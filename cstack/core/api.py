"""
core/api.py
Ian Kollipara
2022.11.25

API Class Definition
"""

# Imports
from fastapi import FastAPI, APIRouter


class API:
    def __init__(self) -> None:
        self.app = FastAPI()

    def include_routers(self, routes: dict[str, APIRouter]):
        for path, router in routes.items():
            self.app.include_router(router, prefix=path)
