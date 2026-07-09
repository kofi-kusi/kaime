from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateNotFound, select_autoescape


class TemplateRenderer:
    def __init__(self, template_dir: Path):
        self.template_dir = template_dir
        self.environment = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
            undefined=StrictUndefined,
        )

    def render(self, template_name: str, context: dict[str, Any]) -> str:
        try:
            template = self.environment.get_template(template_name)
        except TemplateNotFound as exc:
            raise ValueError(
                f"Template '{template_name}' was not found in {self.template_dir}",
            ) from exc

        return template.render(**context)
