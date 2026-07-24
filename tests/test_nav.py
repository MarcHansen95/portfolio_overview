import csv
from pathlib import Path

from src.components.nav import build_nav_dataframe, calculate_nav, import_nav_from_csv


def test_calculate_nav_for_each_person_and_combined() -> None:
    entry = {
        "date": "2026-07-21",
        "people": {
            "marc": {"investments": 100, "cash": 20, "debt": 10, "property_value": 5},
            "amina": {"investments": 200, "cash": 30, "debt": 15, "property_value": 10},
        },
    }

    assert calculate_nav(entry, "marc") == 115
    assert calculate_nav(entry, "amina") == 225
    assert calculate_nav(entry, "combined") == 340


def test_build_nav_dataframe_uses_dates_and_totals() -> None:
    entries = [
        {
            "date": "2026-07-21",
            "people": {
                "marc": {"investments": 100, "cash": 20, "debt": 10, "property_value": 5},
                "amina": {"investments": 200, "cash": 30, "debt": 15, "property_value": 10},
            },
        }
    ]

    df = build_nav_dataframe(entries)

    assert list(df.columns) == ["date", "person", "investments", "cash", "debt", "property_value", "total_nav"]
    assert len(df) == 3
    assert df.loc[df["person"] == "marc", "total_nav"].iloc[0] == 115


def test_import_nav_from_csv_reads_monthly_rows_with_year_carried_forward(tmp_path: Path) -> None:
    csv_path = tmp_path / "sample.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["", "2022", "Februar", " kr 100 ", " kr 10 ", " kr 1000 ", " kr 50 ", " kr 1060 ", "", "", "", "2022", "Februar", " kr 200 ", " kr 20 ", " kr 2000 ", " kr 150 ", " kr 2070 ", ""])
        writer.writerow(["", "", "Marts", " kr 110 ", " kr 12 ", " kr 1000 ", " kr 45 ", " kr 1077 ", "", "", "", "Marts", " kr 210 ", " kr 25 ", " kr 2000 ", " kr 140 ", " kr 2095 ", ""])

    entries = import_nav_from_csv(csv_path)
    entries = [entry for entry in entries if entry["date"] in {"2022-02-01", "2022-03-01"}]

    assert [entry["date"] for entry in entries] == ["2022-02-01", "2022-03-01"]
    assert entries[0]["people"]["marc"]["investments"] == 100.0
    assert entries[0]["people"]["amina"]["cash"] == 20.0
    assert entries[1]["people"]["amina"]["debt"] == 2095.0
