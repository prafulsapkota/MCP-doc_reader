import os
import math
from typing import Optional, Generator
from fastmcp import FastMCP
from src.utils import parse_page_range, stream_text_by_sentences

def register_txt_tools(mcp: FastMCP):
    @mcp.tool(name="read_txt", description="Read plain text files and output formatted in Markdown. Optional page_range segments the document into pages (~30 lines per page).")
    def read_txt(file_path: str, page_range: Optional[str] = None) -> str:
        """Reads TXT file and outputs Markdown."""
        if not os.path.exists(file_path):
            return f"**Error:** File not found at `{file_path}`"
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
                
            line_size = 30
            total_pages = math.ceil(len(lines) / line_size) if lines else 1
            pages_to_read = parse_page_range(page_range, total_pages)
            
            output = []
            output.append(f"# Text File: {os.path.basename(file_path)}")
            output.append(f"*Total Pages (30 lines/page):* {total_pages}\n---")
            
            for p_idx in pages_to_read:
                start_idx = p_idx * line_size
                end_idx = min(start_idx + line_size, len(lines))
                page_lines = lines[start_idx:end_idx]
                
                output.append(f"## Page {p_idx + 1}")
                output.append("```text")
                output.append("".join(page_lines).strip())
                output.append("```\n")
                
            return "\n".join(output)
        except Exception as e:
            return f"**Error reading TXT file:** {str(e)}"

    @mcp.tool(name="stream_txt", description="Stream text file sentence-by-sentence in Markdown.")
    def stream_txt(file_path: str, page_range: Optional[str] = None) -> Generator[str, None, None]:
        """Streams TXT file sentence-by-sentence in Markdown."""
        if not os.path.exists(file_path):
            yield f"**Error:** File not found at `{file_path}`"
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
                
            line_size = 30
            total_pages = math.ceil(len(lines) / line_size) if lines else 1
            pages_to_read = parse_page_range(page_range, total_pages)
            
            yield f"# Streaming Text File: {os.path.basename(file_path)}\n"
            
            for p_idx in pages_to_read:
                yield f"\n## Page {p_idx + 1}\n"
                start_idx = p_idx * line_size
                end_idx = min(start_idx + line_size, len(lines))
                page_text = "".join(lines[start_idx:end_idx])
                
                for sentence in stream_text_by_sentences(page_text):
                    yield sentence
        except Exception as e:
            yield f"**Error streaming TXT file:** {str(e)}"

    @mcp.tool(name="read_txt_data", description="Read plain text file passed directly as a base64-encoded string. Optional file_name is for context. Optional page_range segments the document into pages (~30 lines per page).")
    def read_txt_data(file_content_b64: str, file_name: Optional[str] = None, page_range: Optional[str] = None) -> str:
        """Reads plain text file from base64 string and outputs formatted in Markdown."""
        try:
            from src.utils import decode_b64_to_stream
            stream = decode_b64_to_stream(file_content_b64)
            text = stream.getvalue().decode('utf-8', errors='replace')
            lines = text.splitlines(keepends=True)
                
            line_size = 30
            total_pages = math.ceil(len(lines) / line_size) if lines else 1
            pages_to_read = parse_page_range(page_range, total_pages)
            
            display_name = file_name if file_name else "Uploaded Text File"
            output = []
            output.append(f"# Text File: {display_name}")
            output.append(f"*Total Pages (30 lines/page):* {total_pages}\n---")
            
            for p_idx in pages_to_read:
                start_idx = p_idx * line_size
                end_idx = min(start_idx + line_size, len(lines))
                page_lines = lines[start_idx:end_idx]
                
                output.append(f"## Page {p_idx + 1}")
                output.append("```text")
                output.append("".join(page_lines).strip())
                output.append("```\n")
                
            return "\n".join(output)
        except Exception as e:
            return f"**Error reading TXT data:** {str(e)}"

    @mcp.tool(name="stream_txt_data", description="Stream text file sentence-by-sentence in Markdown from base64-encoded string.")
    def stream_txt_data(file_content_b64: str, file_name: Optional[str] = None, page_range: Optional[str] = None) -> Generator[str, None, None]:
        """Streams text file sentence-by-sentence in Markdown from base64 string."""
        try:
            from src.utils import decode_b64_to_stream
            stream = decode_b64_to_stream(file_content_b64)
            text = stream.getvalue().decode('utf-8', errors='replace')
            lines = text.splitlines(keepends=True)
                
            line_size = 30
            total_pages = math.ceil(len(lines) / line_size) if lines else 1
            pages_to_read = parse_page_range(page_range, total_pages)
            
            display_name = file_name if file_name else "Uploaded Text File"
            yield f"# Streaming Text File: {display_name}\n"
            
            for p_idx in pages_to_read:
                yield f"\n## Page {p_idx + 1}\n"
                start_idx = p_idx * line_size
                end_idx = min(start_idx + line_size, len(lines))
                page_text = "".join(lines[start_idx:end_idx])
                
                for sentence in stream_text_by_sentences(page_text):
                    yield sentence
        except Exception as e:
            yield f"**Error streaming TXT data:** {str(e)}"
