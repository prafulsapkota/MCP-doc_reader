from fastmcp import FastMCP
from src.pdf import register_pdf_tools
from src.docx import register_docx_tools
from src.excel import register_excel_tools
from src.tabular import register_tabular_tools
from src.txt import register_txt_tools

# Initialize FastMCP Server
mcp = FastMCP("DocReaderMCP")

# Register all sub-modules
register_pdf_tools(mcp)
register_docx_tools(mcp)
register_excel_tools(mcp)
register_tabular_tools(mcp)
register_txt_tools(mcp)

if __name__ == "__main__":
    mcp.run()