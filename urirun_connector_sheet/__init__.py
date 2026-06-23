"""sheet:// connector — URI spreadsheet I/O (XLSX via openpyxl, CSV via stdlib)."""
from .core import SHEET, read, write, info, main, urirun_bindings
__all__ = ["SHEET", "read", "write", "info", "main", "urirun_bindings"]
