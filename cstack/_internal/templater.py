"""
templater.py
Ian Kollipara
2022.11.25

Jinja2 Templater
"""

from typing import Any
from jinja2 import Environment, PackageLoader

_environment = Environment(loader=PackageLoader("cstack"))


def render(template_name: str, template_args: dict[str, Any]):
    return _environment.get_template(template_name).render(template_args)
