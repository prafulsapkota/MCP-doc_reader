# DocReaderMCP Server

A FastMCP server designed to read and stream various file formats commonly used in organizations (PDF, DOCX, Excel XLSX, CSV, TSV, TXT). It outputs formatted Markdown and supports both segment/page limits and item streaming.

## Features

- **Document Formats Supported**:
  - `PDF`: Pages parsed and converted to text.
  - `DOCX`: Paragraphs segmented into logical page blocks.
  - `Excel (XLSX/XLS)`: Targeted sheet names or first sheet parsed.
  - `CSV & TSV`: Tables outputted in Markdown format.
  - `TXT`: Plain text paginated into logical blocks.
- **Reading Options**:
  - Optional `page_range` parameter (e.g. `1-3`, `2`) to select specific pages.
  - Optional `sheet_name` parameter for Excel files.
- **Streaming Options**:
  - **Text-Style Documents** (PDF, DOCX, TXT): Streamed sentence-by-sentence.
  - **Tabular Documents** (Excel, CSV, TSV): Streamed row-by-row as Markdown table rows.
- **Docker Ready**: Built with `python:3.13.3-slim`.

---

## Tools Reference

| Tool Name | Parameters | Description |
|---|---|---|
| `read_pdf` | `file_path` (str), `page_range` (Optional[str]) | Read PDF file pages |
| `stream_pdf` | `file_path` (str), `page_range` (Optional[str]) | Stream PDF sentences |
| `read_docx` | `file_path` (str), `page_range` (Optional[str]) | Read DOCX paragraphs by page |
| `stream_docx` | `file_path` (str), `page_range` (Optional[str]) | Stream DOCX sentences |
| `read_excel` | `file_path` (str), `sheet_name` (Optional[str]) | Read sheet to Markdown table |
| `stream_excel`| `file_path` (str), `sheet_name` (Optional[str]) | Stream sheet row-by-row |
| `read_csv` | `file_path` (str) | Read CSV to Markdown table |
| `stream_csv` | `file_path` (str) | Stream CSV row-by-row |
| `read_tsv` | `file_path` (str) | Read TSV to Markdown table |
| `stream_tsv` | `file_path` (str) | Stream TSV row-by-row |
| `read_txt` | `file_path` (str), `page_range` (Optional[str]) | Read TXT by page |
| `stream_txt` | `file_path` (str), `page_range` (Optional[str]) | Stream TXT sentences |

---

## Installation & Setup

### Local Run (Venv / System Python)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server in standard mode:
   ```bash
   python main.py run
   ```
   Or in development mode:
   ```bash
   python main.py dev
   ```

### Running with Docker

1. Build and start the container:
   ```bash
   docker compose up --build
   ```
2. By default, the container mounts a local `./data` directory to `/data` in the container. Put your organizational documents in `./data` to read them via the container.
