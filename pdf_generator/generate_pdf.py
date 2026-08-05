from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright
import os


def generate_pdf(report_data):

    template_dir = os.path.join(
        os.path.dirname(__file__),
        "templates"
    )


    env = Environment(
        loader=FileSystemLoader(template_dir)
    )


    template = env.get_template(
        "report.html"
    )


    # Insert report JSON into HTML
    html_content = template.render(
        **report_data
    )


    output_path = "Startup_Validation_Report.pdf"


    with sync_playwright() as p:

        browser = p.chromium.launch()

        page = browser.new_page()

        page.set_content(
            html_content
        )


        page.pdf(
            path=output_path,
            format="A4",
            print_background=True
        )


        browser.close()


    return output_path