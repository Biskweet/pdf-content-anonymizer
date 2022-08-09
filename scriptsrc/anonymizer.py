import os
import re

import fitz
import requests


def process_all_files(function, path):
    dest = path.strip("/").rsplit("/", 1)[1]
    if function == "multiple":
        # Selecting all PDF files in `path`
        files = [file for file in os.listdir(path) if file[-4:].upper() == ".PDF"]

        for i, file in enumerate(files):
            try:
                pdf = fitz.open(path + "/" + file)                                   # type: ignore
            except (fitz.fitz.FileDataError, fitz.fitz.FileNotFoundError) as error:  # type: ignore
                raise SystemExit(f"File was not found or is corrupted. Please fix your input (error: {error}).")

            text = get_text(pdf)
            # sensitive_data = extract_sensitive_data(text)
            sensitive_data = {}
            replacing_map = assign_aliases(sensitive_data)
            overwrite_document(pdf, replacing_map)

            pdf.save("anonymized-pdfs/" + dest + '/' + file)

    elif function == "single":
        pdf = fitz.open(path)  # type: ignore
        text = get_text(pdf)
        # sensitive_data = extract_sensitive_data(text)
        sensitive_data = {}
        replacing_map = assign_aliases(sensitive_data)
        overwrite_document(pdf, replacing_map)
        pdf.save("anonymized-pdfs/" + dest)


def get_text(document):
    sentences = []
    for page in document:
        sentences += re.split("\!|\.|\;|\?", page.get_text().replace("\n", " "))

    sentences = map(lambda sentence: sentence.strip("\n "), sentences)
    sentences = list(filter(lambda sentence: len(sentence) > 0, sentences))

    for i in range(len(sentences)):
        while sentences[i].find("  ") != -1:
            sentences[i] = sentences[i].replace("  ", " ")

    return "\n".join(sentences)


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
            if category.upper() == "UNKNOWN WORDS":
                prefix = '?'

            # Assigning a new unique alias to each element *if it isn't seen already*
            aliases.setdefault(element, prefix + ('#' + hex(i)).rjust(len(element) - 10, '#'))

    return aliases


def overwrite_document(document, data):
    for page in document:
        for key in data:
            for occurence in page.search_for(key):
                width = occurence.x1 - occurence.x0
                height = occurence.y1 - occurence.y0

                mask = fitz.Rect(occurence.x0, occurence.y0 + height * 0.1, occurence.x1, occurence.y1 - height * 0.1)

                page.add_redact_annot(mask, fill=(0, 0, 0))                                        # draws rectangle
                page.apply_redactions()                                                            # deletes old text
                page.add_freetext_annot(mask, data[key], fontsize=10, text_color=(255, 255, 255))  # writes new alias


if __name__ == "__main__":
    file = input("Select a PDF file: ")
    if file[-4:].upper() != "PDF":
        file += ".pdf"
