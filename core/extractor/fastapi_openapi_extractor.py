from collections import defaultdict
from fastapi.routing import APIRoute


def extract_fastapi_openapi(app):
    openapi_schema = app.openapi()
    paths = openapi_schema.get("paths", {})
    grouped_routes = defaultdict(list)

    for path, methods in paths.items():
        for method, details in methods.items():
            summary = details.get("summary", "No summary provided")
            operation_id = details.get("operationId", "unknown")
            tags = details.get("tags", [])
            parameters = details.get("parameters", [])
            request_body = details.get("requestBody", {})
            responses = details.get("responses", {})

            # Extract simplified request body
            request_body_schema = None
            if request_body:
                content = request_body.get("content", {})
                json_body = content.get("application/json")
                if json_body:
                    request_body_schema = json_body.get("schema")

            # Extract response schemas
            response_schemas = {}
            for status_code, resp in responses.items():
                schema = None
                if "content" in resp:
                    content = resp["content"].get("application/json")
                    if content:
                        schema = content.get("schema")
                response_schemas[status_code] = {
                    "description": resp.get("description"),
                    "schema": schema
                }

            group = path.strip("/").split("/")[0] or "root"

            grouped_routes[group].append({
                "path": path,
                "methods": [method.upper()],
                "summary": summary,
                "tags": tags,
                "endpoint": operation_id,
                "parameters": parameters,
                "request_body": request_body_schema,
                "response_schema": response_schemas,
                "docstring": None  # Not available via OpenAPI
            })

    return grouped_routes
