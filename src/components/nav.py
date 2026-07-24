"""Net asset value tracking helpers for the Streamlit app."""

from __future__ import annotations

import csv
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st


PERSONS = ["marc", "amina", "combined"]


NAV_DATA_FILE = Path(__file__).resolve().parents[2] / "nav_data.json"


def _ensure_nav_file() -> Path:
    """Create the NAV JSON file if it does not yet exist."""
    if not NAV_DATA_FILE.exists():
        NAV_DATA_FILE.write_text("[]", encoding="utf-8")
    return NAV_DATA_FILE


def load_nav_entries() -> list[dict[str, Any]]:
    """Load all NAV entries from the JSON store."""
    path = _ensure_nav_file()
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if isinstance(data, list):
        return data
    return []


def save_nav_entries(entries: list[dict[str, Any]]) -> None:
    """Persist NAV entries to the JSON store."""
    path = _ensure_nav_file()
    with path.open("w", encoding="utf-8") as handle:
        json.dump(entries, handle, indent=2)
        handle.write("\n")


def _parse_currency(value: str | None) -> float:
    """Parse Danish currency strings like 'kr 248.444' into a float."""
    if value is None:
        return 0.0

    cleaned = re.sub(r"[^0-9,.-]", "", str(value).strip())
    if not cleaned:
        return 0.0

    if "," in cleaned and "." in cleaned:
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        cleaned = cleaned.replace(",", ".")

    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _parse_month(month_name: str | None) -> int:
    """Convert a Danish month name to a numeric month."""
    if not month_name:
        return 1

    month_map = {
        "januar": 1,
        "februar": 2,
        "marts": 3,
        "april": 4,
        "maj": 5,
        "juni": 6,
        "juli": 7,
        "august": 8,
        "september": 9,
        "oktober": 10,
        "november": 11,
        "december": 12,
    }
    return month_map.get(str(month_name).strip().lower(), 1)


def import_nav_from_csv(csv_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Import monthly NAV data from the provided CSV file into the JSON format used by the app."""
    source_path = Path(csv_path or Path(__file__).resolve().parents[2] / "Privat formue - Samlet.csv")
    entries: list[dict[str, Any]] = []

    with source_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))

    current_year: str | None = None
    month_map = {
        "januar": 1,
        "februar": 2,
        "marts": 3,
        "april": 4,
        "maj": 5,
        "juni": 6,
        "juli": 7,
        "august": 8,
        "september": 9,
        "oktober": 10,
        "november": 11,
        "december": 12,
    }

    for row in rows:
        if not row:
            continue

        if len(row) > 1 and row[1].strip().isdigit():
            current_year = row[1].strip()

        month = (row[2].strip() if len(row) > 2 else "").lower()
        if month not in month_map:
            continue

        if current_year is None:
            continue

        try:
            year_int = int(current_year)
            month_int = month_map[month]
        except ValueError:
            continue

        entry = {
            "date": f"{year_int:04d}-{month_int:02d}-01",
            "people": {
                "marc": {
                    "investments": _parse_currency(row[3] if len(row) > 3 else None),
                    "cash": _parse_currency(row[4] if len(row) > 4 else None),
                    "property_value": _parse_currency(row[5] if len(row) > 5 else None),
                    "debt": _parse_currency(row[6] if len(row) > 6 else None),
                },
                "amina": {
                    "investments": _parse_currency(row[13] if len(row) > 13 else None),
                    "cash": _parse_currency(row[14] if len(row) > 14 else None),
                    "property_value": _parse_currency(row[15] if len(row) > 15 else None),
                    "debt": _parse_currency(row[16] if len(row) > 16 else None),
                },
            },
        }
        entries.append(entry)

    # Merge with any existing file data, preserving manual edits when dates overlap.
    existing_entries = load_nav_entries()
    by_date = {entry["date"]: entry for entry in existing_entries if entry.get("date")}
    for entry in entries:
        by_date[entry["date"]] = entry

    ordered_entries = [by_date[key] for key in sorted(by_date)]
    return ordered_entries


def calculate_nav(entry: dict[str, Any], person: str = "combined") -> float:
    """Calculate the net asset value for a specific person or the combined total."""
    if person == "combined":
        values = entry.get("people", {})
        total = 0.0
        for person_name in ("marc", "amina"):
            person_data = values.get(person_name, {})
            total += calculate_nav(entry, person_name)
        return total

    person_data = entry.get("people", {}).get(person, {})
    investments = float(person_data.get("investments", 0) or 0)
    cash = float(person_data.get("cash", 0) or 0)
    debt = float(person_data.get("debt", 0) or 0)
    property_value = float(person_data.get("property_value", 0) or 0)
    return investments + cash - debt + property_value


def build_nav_dataframe(entries: list[dict[str, Any]]) -> pd.DataFrame:
    """Convert stored NAV entries into a long-form DataFrame for charts and tables."""
    records: list[dict[str, Any]] = []
    for entry in entries:
        entry_date = entry.get("date")
        if not entry_date:
            continue

        for person in PERSONS:
            person_data = entry.get("people", {}).get(person, {}) if person != "combined" else {}
            if person != "combined":
                records.append(
                    {
                        "date": entry_date,
                        "person": person,
                        "investments": float(person_data.get("investments", 0) or 0),
                        "cash": float(person_data.get("cash", 0) or 0),
                        "debt": float(person_data.get("debt", 0) or 0),
                        "property_value": float(person_data.get("property_value", 0) or 0),
                        "total_nav": calculate_nav(entry, person),
                    }
                )
            else:
                records.append(
                    {
                        "date": entry_date,
                        "person": "combined",
                        "investments": float(entry.get("people", {}).get("marc", {}).get("investments", 0) or 0)
                        + float(entry.get("people", {}).get("amina", {}).get("investments", 0) or 0),
                        "cash": float(entry.get("people", {}).get("marc", {}).get("cash", 0) or 0)
                        + float(entry.get("people", {}).get("amina", {}).get("cash", 0) or 0),
                        "debt": float(entry.get("people", {}).get("marc", {}).get("debt", 0) or 0)
                        + float(entry.get("people", {}).get("amina", {}).get("debt", 0) or 0),
                        "property_value": float(entry.get("people", {}).get("marc", {}).get("property_value", 0) or 0)
                        + float(entry.get("people", {}).get("amina", {}).get("property_value", 0) or 0),
                        "total_nav": calculate_nav(entry, "combined"),
                    }
                )

    if not records:
        return pd.DataFrame(columns=["date", "person", "investments", "cash", "debt", "property_value", "total_nav"])

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values(["person", "date"]).reset_index(drop=True)


def render_nav_tab() -> None:
    """Render the NAV overview and entry form as two tabs."""
    st.subheader("💰 Net Asset Value")
    st.caption("Lock in values for Marc and Amina by date, and track both the individual and combined NAV over time.")

    entries = load_nav_entries()
    overview_tab, entry_tab = st.tabs(["📊 Overview", "➕ Add Data"])

    with overview_tab:
        if not entries:
            st.info("No NAV history yet. Add your first locked-in values in the Add Data tab.")
            return

        df = build_nav_dataframe(entries)
        person_filter = st.selectbox("Show", ["combined", "marc", "amina"], format_func=lambda value: value.title())
        filtered_df = df[df["person"] == person_filter].copy()
        latest = filtered_df.iloc[-1]

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Latest date", latest["date"].strftime("%Y-%m-%d"))
        with col2:
            st.metric("Investments", f"{latest['investments']:,.0f}")
        with col3:
            st.metric("Cash", f"{latest['cash']:,.0f}")
        with col4:
            st.metric("Debt", f"{latest['debt']:,.0f}")
        with col5:
            st.metric("Total NAV", f"{latest['total_nav']:,.0f}")

        display_df = filtered_df.rename(
            columns={
                "investments": "Investments",
                "cash": "Cash",
                "debt": "Debt",
                "property_value": "Property Value",
                "total_nav": "Total NAV",
            }
        )
        st.dataframe(display_df[["date", "Investments", "Cash", "Debt", "Property Value", "Total NAV"]], hide_index=True)

        chart_df = filtered_df.set_index("date")[["investments", "cash", "debt", "property_value", "total_nav"]]
        chart_df.columns = ["Investments", "Cash", "Debt", "Property Value", "Total NAV"]
        st.line_chart(chart_df)

    with entry_tab:
        st.write("Enter the values you want to lock in for a specific date for Marc and Amina.")

        with st.form("nav_entry_form", clear_on_submit=False):
            entry_date = st.date_input("Date", value=date.today())
            st.subheader("Marc")
            marc_investments = st.number_input("Marc investments", value=0.0, step=1000.0, format="%.2f", key="marc_investments")
            marc_cash = st.number_input("Marc cash", value=0.0, step=1000.0, format="%.2f", key="marc_cash")
            marc_debt = st.number_input("Marc debt", value=0.0, step=1000.0, format="%.2f", key="marc_debt")
            marc_property_value = st.number_input("Marc property value", value=0.0, step=1000.0, format="%.2f", key="marc_property_value")

            st.subheader("Amina")
            amina_investments = st.number_input("Amina investments", value=0.0, step=1000.0, format="%.2f", key="amina_investments")
            amina_cash = st.number_input("Amina cash", value=0.0, step=1000.0, format="%.2f", key="amina_cash")
            amina_debt = st.number_input("Amina debt", value=0.0, step=1000.0, format="%.2f", key="amina_debt")
            amina_property_value = st.number_input("Amina property value", value=0.0, step=1000.0, format="%.2f", key="amina_property_value")

            submitted = st.form_submit_button("💾 Push to production")

            if submitted:
                new_entry = {
                    "date": entry_date.strftime("%Y-%m-%d"),
                    "people": {
                        "marc": {
                            "investments": float(marc_investments),
                            "cash": float(marc_cash),
                            "debt": float(marc_debt),
                            "property_value": float(marc_property_value),
                        },
                        "amina": {
                            "investments": float(amina_investments),
                            "cash": float(amina_cash),
                            "debt": float(amina_debt),
                            "property_value": float(amina_property_value),
                        },
                    },
                }
                entries.append(new_entry)
                save_nav_entries(entries)
                st.success(f"Saved NAV entry for {new_entry['date']}.")
                st.rerun()
