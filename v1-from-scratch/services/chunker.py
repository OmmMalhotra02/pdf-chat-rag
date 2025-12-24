chunk_size = 200
overlap = 15

def chunk_pages(pages: list[dict]) -> list[dict]:
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    chunks: list = []

    for page in pages:
        start = 0
        text = page["page_text"]
        chunk_index = 0

        while start<len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()

            if not chunk_text:
                break

            chunks.append({
                "chunk_id": f"{page['page_number']}_{chunk_index}", 
                "page_number": page["page_number"],
                "text": chunk_text
                })
            start = end-overlap
            chunk_index += 1
    return chunks