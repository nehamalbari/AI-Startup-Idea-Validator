def validate_pipeline_output(result):
    """
    Validate the final output of the agent pipeline.
    """

    if not result:
        return False, "Pipeline returned an empty result."

    if not isinstance(result, dict):
        return False, "Pipeline output must be a dictionary."

    if "report" not in result:
        return False, "Final report is missing."

    if not result["report"]:
        return False, "Final report is empty."

    if "pdf" not in result:
        return False, "PDF output is missing."

    return True, "Output passed guardrail."