# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.
"""Kontrakt connectora sheet konformuje i pokrywa KAŻDĄ trasę handlera.

Łapie dryf między deklaracją (`contracts.json`) a kodem: jeśli ktoś doda/zmieni handler
albo złamie efekt↔czasownik/przykłady, ten test czerwienieje. Pomija się czysto bez
pakietu `urirun-contract` (instalacja samego connectora poza monorepo)."""
from __future__ import annotations

import json
import os

import pytest

conform = pytest.importorskip("urirun_contract").conform
Contract = pytest.importorskip("urirun_contract").Contract

PKG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "urirun_connector_sheet")
CONTRACTS = os.path.join(PKG, "contracts.json")


def _load() -> dict:
    doc = json.load(open(CONTRACTS))
    return {r: Contract(version=c["version"], effect=c["effect"], reversible=c["reversible"],
                        inp=c["inp"], out=c["out"], errors=tuple(c["errors"]),
                        examples=tuple(c["examples"]))
            for r, c in doc["contracts"].items()}


def test_contract_conforms():
    conform(_load())  # efekt↔czasownik, wzajemny inverse, przykłady spełniają in+out


def test_every_handler_route_has_a_contract():
    """Każda trasa `@SHEET.handler(...)` w core.py ma wpis w contracts.json (brak białych plam)."""
    core = open(os.path.join(PKG, "core.py"), encoding="utf-8").read()
    discover = pytest.importorskip("urirun_contract.contract_scaffold").discover_routes
    declared = set(json.load(open(CONTRACTS))["contracts"])
    for route in discover(core):
        assert route in declared, f"trasa {route!r} z core.py nie ma kontraktu"
