import os
import pandas as pd
from typing import Generator
from fastmcp import FastMCP
from src.excel import format_df_as_markdown
from typing import Optional


def register_tabular_tools(mcp: FastMCP):
    @mcp.tool(name="read_csv", description="Read CSV files and output as a Markdown table.")
    def read_csv(file_path: str) -> str:
        """Reads CSV and outputs Markdown table."""
        if not os.path.exists(file_path):
            return f"**Error:** File not found at `{file_path}`"
        
        try:
            df = pd.read_csv(file_path)
            md_table = format_df_as_markdown(df)
            return f"# CSV: {os.path.basename(file_path)}\n---\n{md_table}"
        except Exception as e:
            return f"**Error reading CSV:** {str(e)}"

    @mcp.tool(name="stream_csv", description="Stream CSV file row-by-row as Markdown table rows.")
    def stream_csv(file_path: str) -> Generator[str, None, None]:
        """Streams CSV rows."""
        if not os.path.exists(file_path):
            yield f"**Error:** File not found at `{file_path}`"
            return
            
        try:
            df = pd.read_csv(file_path)
            df_clean = df.fillna("").astype(str)
            
            yield f"# Streaming CSV: {os.path.basename(file_path)}\n\n"
            headers = list(df_clean.columns)
            yield "| " + " | ".join(headers) + " |\n"
            yield "| " + " | ".join(["---"] * len(headers)) + " |\n"
            
            for _, row in df_clean.iterrows():
                yield "| " + " | ".join(row.values) + " |\n"
        except Exception as e:
            yield f"**Error streaming CSV:** {str(e)}"

    @mcp.tool(name="read_tsv", description="Read TSV files and output as a Markdown table.")
    def read_tsv(file_path: str) -> str:
        """Reads TSV and outputs Markdown table."""
        if not os.path.exists(file_path):
            return f"**Error:** File not found at `{file_path}`"
        
        try:
            df = pd.read_csv(file_path, sep='\t')
            md_table = format_df_as_markdown(df)
            return f"# TSV: {os.path.basename(file_path)}\n---\n{md_table}"
        except Exception as e:
            return f"**Error reading TSV:** {str(e)}"

    @mcp.tool(name="stream_tsv", description="Stream TSV file row-by-row as Markdown table rows.")
    def stream_tsv(file_path: str) -> Generator[str, None, None]:
        """Streams TSV rows."""
        if not os.path.exists(file_path):
            yield f"**Error:** File not found at `{file_path}`"
            return
            
        try:
            df = pd.read_csv(file_path, sep='\t')
            df_clean = df.fillna("").astype(str)
            
            yield f"# Streaming TSV: {os.path.basename(file_path)}\n\n"
            headers = list(df_clean.columns)
            yield "| " + " | ".join(headers) + " |\n"
            yield "| " + " | ".join(["---"] * len(headers)) + " |\n"
            
            for _, row in df_clean.iterrows():
                yield "| " + " | ".join(row.values) + " |\n"
        except Exception as e:
            yield f"**Error streaming TSV:** {str(e)}"

    @mcp.tool(name="read_csv_data", description="Read CSV file passed directly as base64-encoded string. Optional file_name is for context.")
    def read_csv_data(file_content_b64: str, file_name: Optional[str] = None) -> str:
        """Reads CSV from base64 content and outputs Markdown table."""
        try:
            from src.utils import decode_b64_to_stream
            stream = decode_b64_to_stream(file_content_b64)
            df = pd.read_csv(stream)
            md_table = format_df_as_markdown(df)
            display_name = file_name if file_name else "Uploaded CSV"
            return f"# CSV: {display_name}\n---\n{md_table}"
        except Exception as e:
            return f"**Error reading CSV data:** {str(e)}"

    @mcp.tool(name="stream_csv_data", description="Stream CSV file row-by-row as Markdown table rows from base64-encoded string.")
    def stream_csv_data(file_content_b64: str, file_name: Optional[str] = None) -> Generator[str, None, None]:
        """Streams CSV rows from base64 string."""
        try:
            from src.utils import decode_b64_to_stream
            stream = decode_b64_to_stream(file_content_b64)
            df = pd.read_csv(stream)
            df_clean = df.fillna("").astype(str)
            
            display_name = file_name if file_name else "Uploaded CSV"
            yield f"# Streaming CSV: {display_name}\n\n"
            headers = list(df_clean.columns)
            yield "| " + " | ".join(headers) + " |\n"
            yield "| " + " | ".join(["---"] * len(headers)) + " |\n"
            
            for _, row in df_clean.iterrows():
                yield "| " + " | ".join(row.values) + " |\n"
        except Exception as e:
            yield f"**Error streaming CSV data:** {str(e)}"

    @mcp.tool(name="read_tsv_data", description="Read TSV file passed directly as base64-encoded string. Optional file_name is for context.")
    def read_tsv_data(file_content_b64: str, file_name: Optional[str] = None) -> str:
        """Reads TSV from base64 content and outputs Markdown table."""
        try:
            from src.utils import decode_b64_to_stream
            stream = decode_b64_to_stream(file_content_b64)
            df = pd.read_csv(stream, sep='\t')
            md_table = format_df_as_markdown(df)
            display_name = file_name if file_name else "Uploaded TSV"
            return f"# TSV: {display_name}\n---\n{md_table}"
        except Exception as e:
            return f"**Error reading TSV data:** {str(e)}"

    @mcp.tool(name="stream_tsv_data", description="Stream TSV file row-by-row as Markdown table rows from base64-encoded string.")
    def stream_tsv_data(file_content_b64: str, file_name: Optional[str] = None) -> Generator[str, None, None]:
        """Streams TSV rows from base64 string."""
        try:
            from src.utils import decode_b64_to_stream
            stream = decode_b64_to_stream(file_content_b64)
            df = pd.read_csv(stream, sep='\t')
            df_clean = df.fillna("").astype(str)
            
            display_name = file_name if file_name else "Uploaded TSV"
            yield f"# Streaming TSV: {display_name}\n\n"
            headers = list(df_clean.columns)
            yield "| " + " | ".join(headers) + " |\n"
            yield "| " + " | ".join(["---"] * len(headers)) + " |\n"
            
            for _, row in df_clean.iterrows():
                yield "| " + " | ".join(row.values) + " |\n"
        except Exception as e:
            yield f"**Error streaming TSV data:** {str(e)}"
