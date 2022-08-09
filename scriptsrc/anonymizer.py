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
            sensitive_data = {'adresses': [], 'names': ['R.J. Cinquegrana', 'Cinquegrana', 'Cinquegrana', 'Cinquegrana', 'Thus', 'G. L.', 'Robert Mulligan', 'Lynda Connolly', 'Charles Johnson', 'Mulligan', 'Connolly', 'Johnson', 'Cinquegrana'], 'banCard numbers': [], 'dates of birth': ['November 1, 2012', 'year', 'January 1, 2008', '2008 and September 30', 'September 30, 2011', 'time', 'time', 'time', 'may be', 'March 30, 2013', 'time to', '4,000 hours'], 'emails': [], 'phone numbers': [], 'secutiy numbers': [], 'location': ['States', 'Massachusetts', 'States', 'the ten States', 'Minnesota', 'Michigan', 'Massachusetts', 'States', 'Massachusetts', 'Massachusetts', 'Massachusetts', 'Worcester County', 'Massachusetts', 'Judiciary'], 'organisation': ['THE SUPREME JUDICIAL COURT', 'the Boston Globe Spotlight Team', 'the District Court', 'Boston Municipal Court', 'OUI', 'the Supreme Judicial Court', 'Choate, Hall & Stewart LLP', 'OUI', 'OUI', 'Commonwealth', 'CourtView', 'OUI', 'OUI', 'Commonwealth', 'every Regional Administrative Justice', 'District Court', 'OUI', 'eleven Boston Municipal Court', 'OUI', 'the 2 Judiciary', 'Legislature', 'OUI', 'OUI', 'OUI', 'OUI', 'OUI', 'OUI', 'OUI', 'OUI', 'Commonwealth', 'OUI', '.08', 'OUI', 'OUI', 'Analysis Group', 'OUI', 'State', 'OUI', 'OUI', 'OUI', 'Commonwealth', 'OUI', 'Legislature', 'OUI', 'House', 'Senate', 'the Judiciary Committee', 'the Trial Court', 'the District Court Department', 'the Boston Municipal Court', 'OUI', 'the Supreme Judicial Court', 'the District Court', 'Boston Municipal Court', 'OUI', 'Judicial Institute', 'the Standing Advisory Committee', 'the Trial Court', 'Trial Court', 'Choate, Hall & Stewart', "the Globe's Spotlight Team", 'OUI', 'OUI'], 'unknown words': ['SUPREME', 'JUDICIAL', 'COURT', 'November', 'Boston', 'Globe', 'Spotlight', 'Team', 'District', 'Court', 'Boston', 'Municipal', 'Court', 'Departments', 'OUI', 'Justices', 'Supreme', 'Judicial', 'Court', 'R.J.', 'Cinquegrana', 'Choate', 'Hall', 'Stewart', 'LLP', 'Mr.', 'Cinquegrana', 'OUI', 'OUI', 'Commonwealth', 'Report', 'Mr.', 'Cinquegrana', 'MassCourt', 'CourtView', 'OUI', 'January', 'September', 'OUI', 'District', 'Attorney', 'Commonwealth', 'Regional', 'Administrative', 'Justice', 'District', 'Court', 'OUI', 'Boston', 'Municipal', 'Court', 'Justices', 'Report', 'OUI', 'Judiciary', 'Legislature', 'Report', 'Report', 'OUI', 'OUI', 'Report', 'OUI', 'States', 'OUI', 'Massachusetts', 'States', 'States', 'OUI', 'Minnesota', 'Michigan', 'OUI', 'Report', 'OUI', 'OUI', 'Commonwealth', 'Massachusetts', 'States', 'Massachusetts', 'OUI', 'Massachusetts', 'Massachusetts', 'OUI', 'Assistant', 'District', 'Attorneys', 'Report', 'OUI', 'Report', 'Statewide', 'Mr.', 'Cinquegrana', 'Analysis', 'Group', 'Report', 'OUI', 'Report', 'State', 'Worcester', 'County', 'Report', 'Report', 'OUI', 'Judiciary', 'Report', 'Report', 'Report', 'OUI', 'Report', 'Report', 'OUI', 'Commonwealth', 'Thus', 'Report', 'OUI', 'Report', 'Legislature', 'G.', 'L.', 'c.', 'OUI', 'Report', 'Report', 'Governor', 'Speaker', 'House', 'Senate', 'President', 'Chairs', 'Judiciary', 'Committee', 'Judiciary', 'Chief', 'Justice', 'Trial', 'Court', 'Robert', 'Mulligan', 'Chief', 'Justice', 'Lynda', 'Connolly', 'District', 'Court', 'Department', 'Chief', 'Justice', 'Charles', 'Johnson', 'Boston', 'Municipal', 'Court', 'Report', 'OUI', 'Chief', 'Justices', 'Mulligan', 'Connolly', 'Johnson', 'Justices', 'Supreme', 'Judicial', 'Court', 'March', 'District', 'Court', 'Boston', 'Municipal', 'Court', 'Judiciary', 'OUI', 'Report', 'Judicial', 'Institute', 'Report', 'Standing', 'Advisory', 'Committee', 'Rules', 'Criminal', 'Procedure', 'Chief', 'Justice', 'Trial', 'Court', 'Chief', 'Justices', 'Trial', 'Court', 'Justices', 'Mr.', 'Cinquegrana', 'Choate', 'Hall', 'Stewart', 'LLP', 'Massachusetts', 'Report', 'Globe', 'Spotlight', 'Team', 'Report', 'OUI', 'Justices', 'Judiciary', 'OUI']}
            replacing_map = assign_aliases(sensitive_data)
            overwrite_document(pdf, replacing_map)

            pdf.save("anonymized-pdfs/" + dest + '/' + file)

    elif function == "single":
        pdf = fitz.open(path)  # type: ignore
        text = get_text(pdf)
        # sensitive_data = extract_sensitive_data(text)
        sensitive_data = {'adresses': [], 'names': ['R.J. Cinquegrana', 'Cinquegrana', 'Cinquegrana', 'Cinquegrana', 'Thus', 'G. L.', 'Robert Mulligan', 'Lynda Connolly', 'Charles Johnson', 'Mulligan', 'Connolly', 'Johnson', 'Cinquegrana'], 'banCard numbers': [], 'dates of birth': ['November 1, 2012', 'year', 'January 1, 2008', '2008 and September 30', 'September 30, 2011', 'time', 'time', 'time', 'may be', 'March 30, 2013', 'time to', '4,000 hours'], 'emails': [], 'phone numbers': [], 'secutiy numbers': [], 'location': ['States', 'Massachusetts', 'States', 'the ten States', 'Minnesota', 'Michigan', 'Massachusetts', 'States', 'Massachusetts', 'Massachusetts', 'Massachusetts', 'Worcester County', 'Massachusetts', 'Judiciary'], 'organisation': ['THE SUPREME JUDICIAL COURT', 'the Boston Globe Spotlight Team', 'the District Court', 'Boston Municipal Court', 'OUI', 'the Supreme Judicial Court', 'Choate, Hall & Stewart LLP', 'OUI', 'OUI', 'Commonwealth', 'CourtView', 'OUI', 'OUI', 'Commonwealth', 'every Regional Administrative Justice', 'District Court', 'OUI', 'eleven Boston Municipal Court', 'OUI', 'the 2 Judiciary', 'Legislature', 'OUI', 'OUI', 'OUI', 'OUI', 'OUI', 'OUI', 'OUI', 'OUI', 'Commonwealth', 'OUI', '.08', 'OUI', 'OUI', 'Analysis Group', 'OUI', 'State', 'OUI', 'OUI', 'OUI', 'Commonwealth', 'OUI', 'Legislature', 'OUI', 'House', 'Senate', 'the Judiciary Committee', 'the Trial Court', 'the District Court Department', 'the Boston Municipal Court', 'OUI', 'the Supreme Judicial Court', 'the District Court', 'Boston Municipal Court', 'OUI', 'Judicial Institute', 'the Standing Advisory Committee', 'the Trial Court', 'Trial Court', 'Choate, Hall & Stewart', "the Globe's Spotlight Team", 'OUI', 'OUI'], 'unknown words': ['SUPREME', 'JUDICIAL', 'COURT', 'November', 'Boston', 'Globe', 'Spotlight', 'Team', 'District', 'Court', 'Boston', 'Municipal', 'Court', 'Departments', 'OUI', 'Justices', 'Supreme', 'Judicial', 'Court', 'R.J.', 'Cinquegrana', 'Choate', 'Hall', 'Stewart', 'LLP', 'Mr.', 'Cinquegrana', 'OUI', 'OUI', 'Commonwealth', 'Report', 'Mr.', 'Cinquegrana', 'MassCourt', 'CourtView', 'OUI', 'January', 'September', 'OUI', 'District', 'Attorney', 'Commonwealth', 'Regional', 'Administrative', 'Justice', 'District', 'Court', 'OUI', 'Boston', 'Municipal', 'Court', 'Justices', 'Report', 'OUI', 'Judiciary', 'Legislature', 'Report', 'Report', 'OUI', 'OUI', 'Report', 'OUI', 'States', 'OUI', 'Massachusetts', 'States', 'States', 'OUI', 'Minnesota', 'Michigan', 'OUI', 'Report', 'OUI', 'OUI', 'Commonwealth', 'Massachusetts', 'States', 'Massachusetts', 'OUI', 'Massachusetts', 'Massachusetts', 'OUI', 'Assistant', 'District', 'Attorneys', 'Report', 'OUI', 'Report', 'Statewide', 'Mr.', 'Cinquegrana', 'Analysis', 'Group', 'Report', 'OUI', 'Report', 'State', 'Worcester', 'County', 'Report', 'Report', 'OUI', 'Judiciary', 'Report', 'Report', 'Report', 'OUI', 'Report', 'Report', 'OUI', 'Commonwealth', 'Thus', 'Report', 'OUI', 'Report', 'Legislature', 'G.', 'L.', 'c.', 'OUI', 'Report', 'Report', 'Governor', 'Speaker', 'House', 'Senate', 'President', 'Chairs', 'Judiciary', 'Committee', 'Judiciary', 'Chief', 'Justice', 'Trial', 'Court', 'Robert', 'Mulligan', 'Chief', 'Justice', 'Lynda', 'Connolly', 'District', 'Court', 'Department', 'Chief', 'Justice', 'Charles', 'Johnson', 'Boston', 'Municipal', 'Court', 'Report', 'OUI', 'Chief', 'Justices', 'Mulligan', 'Connolly', 'Johnson', 'Justices', 'Supreme', 'Judicial', 'Court', 'March', 'District', 'Court', 'Boston', 'Municipal', 'Court', 'Judiciary', 'OUI', 'Report', 'Judicial', 'Institute', 'Report', 'Standing', 'Advisory', 'Committee', 'Rules', 'Criminal', 'Procedure', 'Chief', 'Justice', 'Trial', 'Court', 'Chief', 'Justices', 'Trial', 'Court', 'Justices', 'Mr.', 'Cinquegrana', 'Choate', 'Hall', 'Stewart', 'LLP', 'Massachusetts', 'Report', 'Globe', 'Spotlight', 'Team', 'Report', 'OUI', 'Justices', 'Judiciary', 'OUI']}
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

                # print(occurence)
                page.add_redact_annot(mask, fill=(0, 0, 0))                                        # draws rectangle
                page.apply_redactions()                                                            # deletes old text
                page.add_freetext_annot(mask, data[key], fontsize=10, text_color=(255, 255, 255))  # writes new alias


if __name__ == "__main__":
    file = input("Select a PDF file: ")
    if file[-4:].upper() != "PDF":
        file += ".pdf"
