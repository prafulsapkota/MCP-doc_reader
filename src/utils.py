from typing import Optional, Generator
import re

def parse_page_range(page_range: Optional[str], total_pages: int) -> range:
    """Parses optional page range string like '1-5', '3', '2-' and returns a range object (0-indexed)."""
    if not page_range:
        return range(0, total_pages)
    
    page_range = page_range.strip()
    if '-' in page_range:
        parts = page_range.split('-')
        start_str = parts[0].strip()
        end_str = parts[1].strip()
        
        start = int(start_str) - 1 if start_str else 0
        end = int(end_str) if end_str else total_pages
        
        # Clamp bounds
        start = max(0, min(start, total_pages))
        end = max(start, min(end, total_pages))
        return range(start, end)
    else:
        try:
            p = int(page_range) - 1
            p = max(0, min(p, total_pages - 1))
            return range(p, p + 1)
        except ValueError:
            return range(0, total_pages)

def stream_text_by_sentences(text: str) -> Generator[str, None, None]:
    """Simple generator to yield text sentence-by-sentence."""
    # Match sentences ending with ., ! or ? followed by whitespace or end of string
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for sentence in sentences:
        s = sentence.strip()
        if s:
            yield s + "\n"
