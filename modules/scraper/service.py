def scrape_and_save(urls: list[str], filepath: str) -> dict:
    """Scrape each URL and overwrite filepath with combined content."""
    # Overwrite file on each ingest to avoid duplicate chunks
    open(filepath, "w").close()

    processed = 0
    errors = {}

    for url in urls:
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(str(soup))
            processed += 1
        except Exception as e:
            errors[url] = str(e)

    return {"processed": processed, "errors": errors}

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks