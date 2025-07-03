from xhtml2pdf import pisa
from rich.console import Console

console = Console()


def generate_pdf(html_content, output_filename):
    try:
        with console.status("Generating PDF..."):
            with open(output_filename, "w+b") as result_file:
                pisa.CreatePDF(html_content, dest=result_file)
    except Exception as e:
        raise
