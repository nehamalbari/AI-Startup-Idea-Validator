from langchain_core.tools import tool

from pdf_generator.generate_pdf import generate_pdf


@tool
def pdf_generation_tool(report_data: dict) -> str:
    """
    Generate the final startup validation PDF report
    from the combined report data.

    Args:
        report_data: Combined output from the startup validation agents.

    Returns:
        Path of the generated PDF file.
    """

    output_path = generate_pdf(report_data)

    return output_path