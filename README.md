# urirun-connector-sheet

**Spreadsheet I/O (XLSX/CSV)** — connector ekosystemu [ifURI / urirun](https://github.com/if-uri/urirun).
Schemat URI: `sheet://`

Read and write XLSX/CSV over sheet:// URIs without libreoffice. CSV via stdlib (always works); XLSX via openpyxl (pure Python). Reads return {columns, rows}; writes take rows and pick CSV/XLSX from the extension, with an optional totals footer. Pairs with invoice://ksef:// to emit accountant-ready Excel.

## Opis

sheet:// makes spreadsheet I/O a first-class URI. sheet://host/file/query/read returns {columns, rows} from a .xlsx (any tab) or .csv — for ingesting bank statements and accounting exports. sheet://host/file/command/write writes a list of row dicts to .xlsx or .csv (chosen by extension), with an optional per-column SUM footer — for turning parsed invoice / KSeF VAT-register rows into an Excel an accountant opens. sheet://host/file/query/info lists sheets + dimensions. CSV needs no extra deps; XLSX needs openpyxl (pip).

## Wymagania

- **python:** urirun
- **optional:** openpyxl for .xlsx (CSV works without it)

## Instalacja (dev)

```bash
pip install -e .
pytest -q
```

## Powiązane

- Rdzeń: [if-uri/urirun](https://github.com/if-uri/urirun)
- Hub connectorów: [connect.ifuri.com](https://connect.ifuri.com)

---
Kategoria: Accounting · Słowa kluczowe: xlsx, csv, excel, openpyxl, spreadsheet, accounting, ksiegowosc, bank-statement · Wydawca: if-uri
