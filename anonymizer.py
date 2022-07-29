try:
    import textract
    from textract import exceptions
except ModuleNotFoundError:
    raise SystemExit("textract module not found. Please install the package using `pip install textract`.")


file = input("Select a PDF file: ")
if file[-4:].upper() != "PDF":
    file += ".pdf"

try:
    content = textract.process(file)
except (exceptions.MissingFileError, exceptions.ShellError) as error:
    raise SystemExit(f"File not found or corrupt, please check your input (error: {error}).")
