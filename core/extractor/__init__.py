def get_extractor(framework, mode="default"):
    """
    Return the appropriate extractor function based on framework and mode.

    :param framework: 'fastapi', 'flask', or 'django'
    :param mode: 'default' or 'openapi' (only applicable to fastapi)
    :return: extractor function
    """
    if framework == "fastapi":
        if mode == "openapi":
            from .fastapi_openapi_extractor import extract_fastapi_openapi as extract_routes
        else:
            from .fastapi_extractor import extract_fastapi as extract_routes
    elif framework == "flask":
        from .flask_extractor import extract_flask as extract_routes
    elif framework == "django":
        from .django_extractor import extract_django as extract_routes
    else:
        raise ValueError("Unsupported framework")

    return extract_routes
