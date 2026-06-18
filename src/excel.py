import os
import pandas as pd
from typing import Optional, Generator
from fastmcp import FastMCP

def format_df_as_markdown(df: pd.DataFrame) -> str:
    """Formats DataFrame as clean Markdown table, handling missing values gracefully."""
    df_clean = df.fillna("").astype(str)
    headers = list(df_clean.columns)
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    rows = []
    for _, row in df_clean.iterrows():
        rows.append("| " + " | ".join(row.values) + " |")
    return "\n".join([header_line, separator_line] + rows)

def register_excel_tools(mcp: FastMCP):
    @mcp.tool(name="read_excel", description="Read Excel files. Optional sheet_name can be specified, else reads the first sheet.")
    def read_excel(file_path: str, sheet_name: Optional[str] = None) -> str:
        """Reads Excel and returns content in Markdown format."""
        if not os.path.exists(file_path):
            return f"**Error:** File not found at `{file_path}`"
        
        try:
            xls = pd.ExcelFile(file_path)
            sheets = xls.sheet_names
            
            target_sheet = sheet_name if sheet_name else sheets[0]
            if target_sheet not in sheets:
                return f"**Error:** Sheet `{target_sheet}` not found. Available sheets: {sheets}"
                
            df = pd.read_excel(xls, sheet_name=target_sheet)
            md_table = format_df_as_markdown(df)
            
            output = [
                f"# Excel Workbook: {os.path.basename(file_path)}",
                f"*Available Sheets:* {sheets}",
                f"*Current Sheet:* **{target_sheet}**\n---",
                md_table
            ]
            return "\n".join(output)
        except Exception as e:
            return f"**Error reading Excel:** {str(e)}"

    @mcp.tool(name="stream_excel", description="Stream Excel file row-by-row formatted as Markdown table rows.")
    def stream_excel(file_path: str, sheet_name: Optional[str] = None) -> Generator[str, None, None]:
        """Streams Excel rows one-by-one."""
        if not os.path.exists(file_path):
            yield f"**Error:** File not found at `{file_path}`"
            return
            
        try:
            xls = pd.ExcelFile(file_path)
            sheets = xls.sheet_names
            
            target_sheet = sheet_name if sheet_name else sheets[0]
            if target_sheet not in sheets:
                yield f"**Error:** Sheet `{target_sheet}` not found. Available sheets: {sheets}"
                return
                
            df = pd.read_excel(xls, sheet_name=target_sheet)
            df_clean = df.fillna("").astype(str)
            
            yield f"# Streaming Excel Sheet: {target_sheet} (from {os.path.basename(file_path)})\n\n"
            
            headers = list(df_clean.columns)
            yield "| " + " | ".join(headers) + " |\n"
            yield "| " + " | ".join(["---"] * len(headers)) + " |\n"
            
            for _, row in df_clean.iterrows():
                yield "| " + " | ".join(row.values) + " |\n"
        except Exception as e:
            yield f"**Error streaming Excel:** {str(e)}"

    @mcp.tool(name="read_excel_data", description="Read Excel workbook passed directly as a base64 encoded string. Optional file_name is for context. Optional sheet_name can be specified, else reads first sheet.")
    def read_excel_data(file_content_b64: str, file_name: Optional[str] = None, sheet_name: Optional[str] = None) -> str:
        """Reads Excel file from base64 content and returns Markdown."""
        try:
            from src.utils import decode_b64_to_stream
            stream = decode_b64_to_stream(file_content_b64)
            xls = pd.ExcelFile(stream)
            sheets = xls.sheet_names
            
            target_sheet = sheet_name if sheet_name else sheets[0]
            if target_sheet not in sheets:
                return f"**Error:** Sheet `{target_sheet}` not found. Available sheets: {sheets}"
                
            df = pd.read_excel(xls, sheet_name=target_sheet)
            md_table = format_df_as_markdown(df)
            
            display_name = file_name if file_name else "Uploaded Workbook"
            output = [
                f"# Excel Workbook: {display_name}",
                f"*Available Sheets:* {sheets}",
                f"*Current Sheet:* **{target_sheet}**\n---",
                md_table
            ]
            return "\n".join(output)
        except Exception as e:
            return f"**Error reading Excel data:** {str(e)}"

    @mcp.tool(name="stream_excel_data", description="Stream Excel workbook sheet rows one-by-one from base64 encoded string.")
    def stream_excel_data(file_content_b64: str, file_name: Optional[str] = None, sheet_name: Optional[str] = None) -> Generator[str, None, None]:
        """Streams Excel rows one-by-one from base64 encoded string."""
        try:
            from src.utils import decode_b64_to_stream
            stream = decode_b64_to_stream(file_content_b64)
            xls = pd.ExcelFile(stream)
            sheets = xls.sheet_names
            
            target_sheet = sheet_name if sheet_name else sheets[0]
            if target_sheet not in sheets:
                yield f"**Error:** Sheet `{target_sheet}` not found. Available sheets: {sheets}"
                return
                
            df = pd.read_excel(xls, sheet_name=target_sheet)
            df_clean = df.fillna("").astype(str)
            
            display_name = file_name if file_name else "Uploaded Workbook"
            yield f"# Streaming Excel Sheet: {target_sheet} (from {display_name})\n\n"
            
            headers = list(df_clean.columns)
            yield "| " + " | ".join(headers) + " |\n"
            yield "| " + " | ".join(["---"] * len(headers)) + " |\n"
            
            for _, row in df_clean.iterrows():
                yield "| " + " | ".join(row.values) + " |\n"
        except Exception as e:
            yield f"**Error streaming Excel data:** {str(e)}"
