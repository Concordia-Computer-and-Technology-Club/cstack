"""
core/middleware.py
Ian Kollipara
2022.11.25

Middleware Closure
"""

# Imports
from typing import Literal
from fastapi import FastAPI


def middleware(middleware_type: Literal["http", "ws"] = "http"):
    def inner(func):
        def wrapped(app: FastAPI):

            return app.middleware(middleware_type)(func)

        return wrapped

    return inner
