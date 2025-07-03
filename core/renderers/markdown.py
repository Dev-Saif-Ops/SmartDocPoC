import json

from cli.utils.helper import AdaptiveProgressManager


def generate_markdown(grouped_routes: dict, progress: AdaptiveProgressManager, task=None) -> str:
    md = "# 📘 API Documentation\n\n"

    # Update progress step without advancing
    progress.update_step("Processing API groups...", advance=False)

    for group_name in grouped_routes.keys():
        routes = grouped_routes[group_name]
        md += f"## 📂 {group_name.capitalize()} Endpoints\n\n"

        for route in routes:
            md += f"### `{route['path']}`\n"
            md += f"- **Methods**: {', '.join(route.get('methods', []))}\n"
            md += f"- **Summary**: {route.get('summary', 'No summary provided')}\n"
            md += f"- **Endpoint**: `{route.get('endpoint', '-')}`\n"

            if params := route.get("parameters"):
                md += "- **Parameters**:\n"
                for param in params:
                    md += f"  - `{param['name']}` ({param['in']}) - {param.get('description', '')}\n"

            if body_schema := route.get("request_body"):
                md += "- **Request Body Schema**:\n"
                md += "```json\n"
                try:
                    parsed = json.loads(body_schema) if isinstance(body_schema, str) else body_schema
                    md += json.dumps(parsed, indent=2)
                except Exception:
                    md += str(body_schema)
                md += "\n```\n"

            if response_schema := route.get("response_model_schema"):
                md += "- **Response Model Schema**:\n"
                md += "```json\n"
                try:
                    parsed = json.loads(response_schema) if isinstance(response_schema, str) else response_schema
                    md += json.dumps(parsed, indent=2)
                except Exception:
                    md += str(response_schema)
                md += "\n```\n"

            if docstring := route.get("docstring"):
                md += f"- **Docstring**:\n  {docstring.strip()}\n"

            md += "\n---\n\n"

    return md
