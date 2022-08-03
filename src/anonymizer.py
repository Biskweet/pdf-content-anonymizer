import os
import fitz
import requests


def process_all_files(path):
    files = os.listdir(path)
    files = [file for file in files if file[-4:].upper() == ".PDF"]

    for file in files:
        try:
            pdf = fitz.open(path + file)                                         # type: ignore
        except (fitz.fitz.FileDataError, fitz.fitz.FileNotFoundError) as error:  # type: ignore
            raise SystemExit(f"File was not found or is corrupted. Please fix your input (error: {error}).")

        text = get_text(pdf)
        sensitive_data = extract_sensitive_data(text)
        replacing_map = assign_aliases(sensitive_data)
        overwrite_document(pdf, replacing_map)

        pdf.save("anonymized-pdfs/" + file)


def get_text(document):
    text = ""
    for page in document:
        text += page.get_text() + "\n"

    return text


def extract_sensitive_data(text):
    response = requests.get("https://url.to.api/", json={"data": text})
    if response.status_code != "200":
        raise SystemExit("Error when trying to reach the API.")

    return response.json()


def assign_aliases(data):
    aliases = dict()

    for category in data:
        prefix = category[:3].upper()

        for i, element in enumerate(data[category]):
            # Assigning a new unique alias to each element *if it isn't seen already*
            aliases.setdefault(element, prefix + "#" + hex(i))

    return aliases


def overwrite_document(document, data):
    for page in document:
        for key in data:
            for occurence in page.search_for(key):
                page.add_redact_annot(occurence)               # mark the text
                page.apply_redactions()
                page.add_freetext_annot(occurence, data[key])  # overwrite


if __name__ == "__main__":
    file = input("Select a PDF file: ")
    if file[-4:].upper() != "PDF":
        file += ".pdf"

    try:
        pdf = fitz.open(file)                                                # type: ignore
    except (fitz.fitz.FileDataError, fitz.fitz.FileNotFoundError) as error:  # type: ignore
        raise SystemExit(f"File was not found or is corrupted. Please fix your input (error: {error}).")

    text = get_text(pdf)
    sensitive_data = extract_sensitive_data(text)
    replacing_map = assign_aliases(sensitive_data)
    overwrite_document(pdf, replacing_map)
    pdf.save("anonymized-pdfs/" + file)
