import sys
import os
import click
from importlib import import_module
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from cli.utils.helper import AdaptiveProgressManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.extractor.flask_extractor import extract_flask
from core.extractor.fastapi_extractor import extract_fastapi
from core.extractor.django_extractor import extract_django
from core.renderers.html import generate_html
from core.renderers.markdown import generate_markdown
from core.renderers.pdf import generate_pdf

console = Console()


@click.group()
def cli():
    """SmartDoc CLI for generating API documentation."""
    pass


@click.command(name="generate")
@click.option(
    "--app", "-a",
    required=True,
    help="App module path (e.g., sample_app.main)"
)
@click.option(
    "--framework", "-f",
    required=True,
    type=click.Choice(["fastapi", "django", "flask"]),
    help="Framework used in the app"
)
@click.option(
    "--output", "-o",
    default="api_docs.md",
    help="Output markdown filename"
)
@click.option(
    "--html", is_flag=True,
    help="Also generate an HTML file"
)
@click.option(
    "--pdf", is_flag=True,
    help="Also generate a PDF file"
)
@click.option(
    "--django-settings",
    help="Django settings module",
    default=None
)
@click.option(
    "--mode",
    type=click.Choice(["default", "openapi"]),
    default="default",
    help="Extraction mode for FastAPI (default or openapi)"
)
def generate(app, framework, output, html, pdf, django_settings, mode):
    """Generate API documentation with adaptive progress display."""

    # Calculate total steps (Load, Extract, Markdown, HTML, PDF)
    total_steps = 3 + (1 if html else 0) + (1 if pdf else 0)

    with AdaptiveProgressManager(total_steps, f"Loading app: {app} (Framework: {framework}, Mode: {mode})") as progress:

        # Step 1: Load app
        try:
            progress.update_step("Loading application module...")
            module = import_module(app.replace("/", ".").rstrip(".py"))
            progress.complete_step("✓ App loaded successfully")
        except Exception as e:
            progress.error_step(f"Failed to load app: {e}")
            sys.exit(1)

        # Step 2: Extract routes
        try:
            progress.update_step("Extracting API routes...")

            if framework == "fastapi":
                app_instance = getattr(module, "app", None)
                if not app_instance:
                    progress.error_step("Could not find FastAPI `app` in the given module")
                    sys.exit(1)

                if mode == "openapi":
                    from core.extractor.fastapi_openapi_extractor import extract_fastapi_openapi
                    routes = extract_fastapi_openapi(app_instance)
                else:
                    routes = extract_fastapi(app_instance)

            elif framework == "django":
                if django_settings:
                    os.environ.setdefault("DJANGO_SETTINGS_MODULE", django_settings)
                    import django
                    django.setup()
                routes = extract_django(module)

            elif framework == "flask":
                app_instance = getattr(module, "app", None)
                if not app_instance:
                    progress.error_step("Could not find Flask `app` in the given module")
                    sys.exit(1)
                routes = extract_flask(app_instance)

            else:
                progress.error_step("Unsupported framework")
                sys.exit(1)

            progress.complete_step("✓ Routes extracted successfully")
        except Exception as e:
            progress.error_step(f"Failed to extract routes: {e}")
            sys.exit(1)

        # Step 3: Generate Markdown
        try:
            progress.update_step("Generating markdown documentation...")
            md_content = generate_markdown(routes, progress, None)
            with open(output, "w", encoding="utf-8") as f:
                f.write(md_content)
            progress.complete_step("✓ Markdown generated successfully")
        except Exception as e:
            progress.error_step(f"Failed to generate markdown: {e}")
            sys.exit(1)

        # Step 4: Optional HTML
        html_content = None
        if html or pdf:
            try:
                progress.update_step("Generating HTML documentation...")
                html_content = generate_html(md_content, output.replace(".md", ""))
                progress.complete_step("✓ HTML generated successfully")
            except Exception as e:
                progress.error_step(f"Failed to generate HTML: {e}")
                sys.exit(1)

        # Step 5: Optional PDF
        if pdf:
            try:
                progress.update_step("Generating PDF documentation...")
                if html_content is None:
                    html_content = generate_html(md_content, output.replace(".md", ""))
                generate_pdf(html_content, output.replace(".md", ".pdf"))
                progress.complete_step("✓ PDF generated successfully")
            except Exception as e:
                progress.error_step(f"Failed to generate PDF: {e}")
                sys.exit(1)

        # Final summary
        progress.finish("🎉 Documentation generated successfully!")
        progress.console.print()
        progress.console.print(f"[bold cyan]📄 Markdown:[/] {output}")
        if html:
            progress.console.print(f"[bold cyan]🌐 HTML:[/] {output.replace('.md', '.html')}")
        if pdf:
            progress.console.print(f"[bold cyan]📄 PDF:[/] {output.replace('.md', '.pdf')}")

        # Save console output for debugging
        progress.console.save_text("console_output.txt")


cli.add_command(generate)

if __name__ == "__main__":
    cli()
