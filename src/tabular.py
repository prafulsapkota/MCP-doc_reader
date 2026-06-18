import os
import pandas as pd
from typing import Generator
from fastmcp import FastMCP
from src.excel import format_df_as_markdown

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
