import fitz

def extract_pdf_text(path):
    text: list[dict[str, int | str]] = []

    with fitz.open(path) as doc:
        for page in doc:
            text.append({"page_number": page.number, "page_text": page.get_text()})
    return text