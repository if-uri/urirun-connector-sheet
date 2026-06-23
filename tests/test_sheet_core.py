"""Offline tests for the sheet connector: CSV round-trip (stdlib), XLSX round-trip + totals (optional)."""
import pytest
import urirun_connector_sheet.core as c


def test_bindings_valid():
    b = c.urirun_bindings()
    assert set(b["bindings"]) == {
        "sheet://host/file/query/read", "sheet://host/file/command/write", "sheet://host/file/query/info"}


def test_csv_round_trip(tmp_path):
    p = str(tmp_path / "r.csv")
    rows = [{"nr": "FV 1", "brutto": 100.0}, {"nr": "FV 2", "brutto": 200.0}]
    w = c.write(path=p, rows=rows, columns=["nr", "brutto"])
    assert w["ok"] and w["rows"] == 2
    r = c.read(path=p)
    assert r["ok"] and r["columns"] == ["nr", "brutto"] and r["rowCount"] == 2
    assert r["rows"][0]["nr"] == "FV 1"


def test_csv_info(tmp_path):
    p = str(tmp_path / "r.csv")
    c.write(path=p, rows=[{"a": 1, "b": 2}], columns=["a", "b"])
    i = c.info(path=p)
    assert i["ok"] and i["kind"] == "csv" and i["columns"] == ["a", "b"]


def test_read_missing_file():
    assert c.read(path="/no/such/file.csv")["ok"] is False


def test_unsupported_extension(tmp_path):
    p = tmp_path / "x.docx"
    p.write_text("x")
    assert c.read(path=str(p))["ok"] is False


def test_xlsx_round_trip_with_totals(tmp_path):
    pytest.importorskip("openpyxl")
    p = str(tmp_path / "f.xlsx")
    rows = [{"nr": "A", "netto": 313.0, "vat": 71.99}, {"nr": "B", "netto": 104.11, "vat": 16.59}]
    w = c.write(path=p, rows=rows, columns=["nr", "netto", "vat"], totals=["netto", "vat"])
    assert w["ok"] and w["bytes"] > 0
    r = c.read(path=p)
    assert r["ok"]
    # last data row is the TOTAL footer
    foot = r["rows"][-1]
    assert foot["nr"] == "TOTAL"
    assert round(foot["netto"], 2) == 417.11 and round(foot["vat"], 2) == 88.58


def test_xlsx_info(tmp_path):
    pytest.importorskip("openpyxl")
    p = str(tmp_path / "f.xlsx")
    c.write(path=p, rows=[{"a": 1}], columns=["a"], sheet="Faktury")
    i = c.info(path=p)
    assert i["ok"] and i["kind"] == "xlsx"
    assert any(s["name"] == "Faktury" for s in i["sheets"])
