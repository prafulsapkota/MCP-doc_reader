import os
from typing import Optional, Generator
import pypdf
from fastmcp import FastMCP
from src.utils import parse_page_range, stream_text_by_sentences

def register_pdf_tools(mcp: FastMCP):
    @mcp.tool(name="read_pdf", description="Read PDF files and convert pages to Markdown. Optional parameter page_range specifies page range like '1-3' or '2'.")
    def read_pdf(file_path: str, page_range: Optional[str] = None) -> str:
        """Reads PDF and outputs Markdown."""
        if not os.path.exists(file_path):
            return f"**Error:** File not found at `{file_path}`"
        
        try:
            reader = pypdf.PdfReader(file_path)
            total_pages = len(reader.pages)
            pages_to_read = parse_page_range(page_range, total_pages)
            
            output = []
            output.append(f"# PDF: {os.path.basename(file_path)}")
            output.append(f"*Total Pages:* {total_pages} (Reading pages: {list(pages_to_read) if page_range else 'all'})\n---")
            
            for idx in pages_to_read:
                page_text = reader.pages[idx].extract_text() or ""
                output.append(f"## Page {idx + 1}\n{page_text.strip()}\n")
                
            return "\n".join(output)
        except Exception as e:
            return f"**Error reading PDF:** {str(e)}"

    @mcp.tool(name="stream_pdf", description="Stream PDF sentences from specified pages (e.g. page_range='1-3') in Markdown.")
    def stream_pdf(file_path: str, page_range: Optional[str] = None) -> Generator[str, None, None]:
        """Streams PDF text sentence-by-sentence in Markdown."""
        if not os.path.exists(file_path):
            yield f"**Error:** File not found at `{file_path}`"
            return
        
        try:
            reader = pypdf.PdfReader(file_path)
            total_pages = len(reader.pages)
            pages_to_read = parse_page_range(page_range, total_pages)
            
            yield f"# Streaming PDF: {os.path.basename(file_path)}\n"
            
            for idx in pages_to_read:
                yield f"\n## Page {idx + 1}\n"
                page_text = reader.pages[idx].extract_text() or ""
                for sentence in stream_text_by_sentences(page_text):
                    yield sentence
        except Exception as e:
            yield f"**Error streaming PDF:** {str(e)}"

    @mcp.tool(name="read_pdf_data", description="Read PDF file passed directly as a base64-encoded string. Optional file_name is for context. Optional page_range specifies page range like '1-3' or '2'.")
    def read_pdf_data(file_content_b64: str, file_name: Optional[str] = None, page_range: Optional[str] = None) -> str:
        """Reads base64-encoded PDF and outputs Markdown."""
        try:
            from src.utils import decode_b64_to_stream
            stream = decode_b64_to_stream(file_content_b64)
            reader = pypdf.PdfReader(stream)
            total_pages = len(reader.pages)
            pages_to_read = parse_page_range(page_range, total_pages)
            
            display_name = file_name if file_name else "Uploaded PDF"
            output = []
            output.append(f"# PDF: {display_name}")
            output.append(f"*Total Pages:* {total_pages} (Reading pages: {list(pages_to_read) if page_range else 'all'})\n---")
            
            for idx in pages_to_read:
                page_text = reader.pages[idx].extract_text() or ""
                output.append(f"## Page {idx + 1}\n{page_text.strip()}\n")
                
            return "\n".join(output)
        except Exception as e:
            return f"**Error reading PDF data:** {str(e)}"

    @mcp.tool(name="stream_pdf_data", description="Stream sentences from a base64-encoded PDF file.")
    def stream_pdf_data(file_content_b64: str, file_name: Optional[str] = None, page_range: Optional[str] = None) -> Generator[str, None, None]:
        """Streams base64-encoded PDF text sentence-by-sentence in Markdown."""
        try:
            from src.utils import decode_b64_to_stream
            stream = decode_b64_to_stream(file_content_b64)
            reader = pypdf.PdfReader(stream)
            total_pages = len(reader.pages)
            pages_to_read = parse_page_range(page_range, total_pages)
            
            display_name = file_name if file_name else "Uploaded PDF"
            yield f"# Streaming PDF: {display_name}\n"
            
            for idx in pages_to_read:
                yield f"\n## Page {idx + 1}\n"
                page_text = reader.pages[idx].extract_text() or ""
                for sentence in stream_text_by_sentences(page_text):
                    yield sentence
        except Exception as e:
            yield f"**Error streaming PDF data:** {str(e)}"
