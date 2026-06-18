from typing import Optional, Generator
import re
import io
import base64

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

def decode_b64_to_stream(b64_str: str) -> io.BytesIO:
    """Decodes a base64 encoded string to an in-memory BytesIO stream, stripping data URL prefixes if present."""
    if "," in b64_str:
        # Strip potential data URL prefix like "data:application/pdf;base64,"
        parts = b64_str.split(",", 1)
        # Check if the prefix has base64 in it to ensure it's a data URL
        if "base64" in parts[0]:
            b64_str = parts[1]
    
    decoded = base64.b64decode(b64_str.strip())
    return io.BytesIO(decoded)
