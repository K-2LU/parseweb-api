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