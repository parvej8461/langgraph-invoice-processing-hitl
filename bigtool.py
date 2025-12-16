
def bigtool_picker(capability: str, context: dict) -> str:
    """
    Select tool dynamically based on capability and context.
    This is a simple rule-based Bigtool implementation.
    """

    if capability == "ocr":
        file_type = context.get("file_type", "pdf")

        if file_type == "pdf":
            return "aws_textract"
        elif file_type == "image":
            return "google_vision"
        else:
            return "tesseract"

    if capability == "erp":
        env = context.get("env", "demo")

        if env == "prod":
            return "sap"
        return "mock_erp"

    if capability == "db":
        return "sqlite"

    return "default_tool"
