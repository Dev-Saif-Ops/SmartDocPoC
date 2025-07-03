from rich.console import Console

console = Console()


def generate_html(md_content, output_basename):
    html = f"""<html>
<head>
    <title>API Docs</title>
</head>
<body>
    <h1>API Documentation</h1>
    <pre>{md_content}</pre>
</body>
</html>
"""
    try:
        with console.status("Generating HTML..."):
            with open(f"{output_basename}.html", "w", encoding="utf-8") as f:
                f.write(html)
        return html  # Return HTML content for PDF generation
    except Exception as e:
        console.print(f"[red]Error generating HTML:[/] {e}")
        raise
