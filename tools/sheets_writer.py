# sheets_writer.py — narrow write surface to the WTS Severity Thresholds Google Sheet.
# Owned by Jarvis (see .claude/agents/jarvis.md §Threshold-Sheet Sync). Reads row 1 every call to
# build a {header_name: column_index_1based} map, so column re-ordering on the sheet is safe as
# long as header names stay constant. Never hardcodes column positions.
#
# Sheet identity is pinned in config/settings.py (THRESHOLDS_SHEET_ID + THRESHOLDS_SHEET_GID).
# Auth uses the existing shared service account with DWD impersonation — the sheet must be
# shared with settings.GOOGLE_IMPERSONATION_EMAIL as Editor before any write succeeds.

import logging
from typing import Optional

import gspread

from config import settings
from tools.google_auth import get_service_account_credentials

logger = logging.getLogger(__name__)

# #note: Read+write scope for Sheets, read-only scope for Drive (Drive is only used by gspread
# to resolve the sheet by ID — no Drive writes happen from this module).
_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
]

# #note: The header in the Metric column that the lookup-by-metric helpers use to find existing rows.
# Stored as a constant so a sheet-header rename only changes one place.
_METRIC_HEADER = "Metric"


# #note: Authenticates with Google using the shared credential helper and returns a gspread client.
# DWD impersonation is required because the sheet lives in the emplicit.co Workspace domain.
def _get_gspread_client() -> gspread.Client:
    creds = get_service_account_credentials(_SCOPES, impersonate=True)
    return gspread.Client(auth=creds)


# #note: Opens the canonical WTS Severity Thresholds worksheet by its pinned ID + GID.
# Returns the gspread Worksheet object. Raises if the sheet is not shared with the impersonation
# user — caller is expected to surface that as a clear error in the Jarvis report.
def get_thresholds_worksheet() -> gspread.Worksheet:
    client = _get_gspread_client()
    spreadsheet = client.open_by_key(settings.THRESHOLDS_SHEET_ID)
    return spreadsheet.get_worksheet_by_id(settings.THRESHOLDS_SHEET_GID)


# #note: Reads row 1 and returns {header_name: column_index_1based}. Blank header cells are skipped.
# This is the foundation of the "match by column name, not hardcoded location" guarantee.
def _build_header_index(worksheet: gspread.Worksheet) -> dict[str, int]:
    headers = worksheet.row_values(1)
    index: dict[str, int] = {}
    for col_idx, name in enumerate(headers, start=1):
        clean = (name or "").strip()
        if clean:
            index[clean] = col_idx
    return index


# #note: Returns every row on the sheet as a list of dicts keyed by header name.
# Skips the header row itself. Empty rows (no values) are excluded so callers can iterate cleanly.
def read_threshold_rows() -> list[dict[str, str]]:
    worksheet = get_thresholds_worksheet()
    records = worksheet.get_all_records()
    return [r for r in records if any(str(v).strip() for v in r.values())]


# #note: Finds the 1-indexed sheet row whose Metric column matches metric_name (case-insensitive,
# trimmed). Returns None if no match. Header row is row 1, so the first data row is row 2.
def find_row_by_metric(metric_name: str) -> Optional[int]:
    worksheet = get_thresholds_worksheet()
    headers = _build_header_index(worksheet)
    if _METRIC_HEADER not in headers:
        raise ValueError(
            f"Sheet is missing required header '{_METRIC_HEADER}' — cannot locate rows by metric."
        )
    metric_col = headers[_METRIC_HEADER]
    target = metric_name.strip().lower()
    col_values = worksheet.col_values(metric_col)
    # #note: enumerate starts at 1 because col_values is the entire column including the header
    for row_idx, value in enumerate(col_values, start=1):
        if row_idx == 1:
            continue  # header row
        if str(value).strip().lower() == target:
            return row_idx
    return None


# #note: Appends a row to the bottom of the sheet. row_data is keyed by header name — any keys
# not present in the sheet's header row are dropped with a warning so a typo doesn't silently
# write to the wrong column. Missing keys are written as empty strings, preserving column alignment.
# Returns the 1-indexed row number where the data was written.
def append_threshold_row(row_data: dict[str, str]) -> int:
    worksheet = get_thresholds_worksheet()
    headers = _build_header_index(worksheet)

    unknown_keys = [k for k in row_data if k not in headers]
    if unknown_keys:
        logger.warning(
            f"append_threshold_row: dropping unknown header keys (typo or sheet drift?): {unknown_keys}"
        )

    # #note: Build a list of values in the exact column order of the sheet, so the row aligns with headers.
    max_col = max(headers.values()) if headers else 0
    values: list[str] = [""] * max_col
    for header_name, col_idx in headers.items():
        if header_name in row_data:
            values[col_idx - 1] = str(row_data[header_name])

    worksheet.append_row(values, value_input_option="USER_ENTERED")

    # #note: append_row doesn't return the row index — re-read to find where it landed.
    # Using col_values on the Metric column is cheap and exact.
    metric = row_data.get(_METRIC_HEADER, "").strip()
    if metric:
        row_idx = find_row_by_metric(metric)
        if row_idx is not None:
            return row_idx
    # Fallback: report the new bottom row.
    return len(worksheet.col_values(headers.get(_METRIC_HEADER, 1)))


# #note: Inserts a row at a specific 1-indexed position, pushing existing rows down.
# Same header-keyed semantics as append_threshold_row. Use this when ordering matters
# (e.g. inserting a new metric inside a category block on the sheet).
def insert_threshold_row(row_data: dict[str, str], row_index: int) -> int:
    if row_index < 2:
        raise ValueError(f"row_index must be >= 2 (row 1 is the header). Got {row_index}.")
    worksheet = get_thresholds_worksheet()
    headers = _build_header_index(worksheet)

    unknown_keys = [k for k in row_data if k not in headers]
    if unknown_keys:
        logger.warning(
            f"insert_threshold_row: dropping unknown header keys: {unknown_keys}"
        )

    max_col = max(headers.values()) if headers else 0
    values: list[str] = [""] * max_col
    for header_name, col_idx in headers.items():
        if header_name in row_data:
            values[col_idx - 1] = str(row_data[header_name])

    worksheet.insert_row(values, index=row_index, value_input_option="USER_ENTERED")
    return row_index


# #note: Updates one or more cells in an existing row, located by metric_name.
# updates is keyed by header name → new value. Returns the row index updated, or None if no match.
# Unknown header keys are dropped with a warning (same defensive behavior as append).
def update_threshold_row(metric_name: str, updates: dict[str, str]) -> Optional[int]:
    worksheet = get_thresholds_worksheet()
    headers = _build_header_index(worksheet)

    row_idx = find_row_by_metric(metric_name)
    if row_idx is None:
        logger.warning(f"update_threshold_row: no row found with {_METRIC_HEADER}='{metric_name}'")
        return None

    cells_to_update: list[gspread.Cell] = []
    for header_name, new_value in updates.items():
        if header_name not in headers:
            logger.warning(
                f"update_threshold_row: dropping unknown header key '{header_name}' (typo or sheet drift?)"
            )
            continue
        cells_to_update.append(
            gspread.Cell(row=row_idx, col=headers[header_name], value=str(new_value))
        )

    if not cells_to_update:
        logger.info(f"update_threshold_row: no valid updates for row {row_idx} — no-op")
        return row_idx

    worksheet.update_cells(cells_to_update, value_input_option="USER_ENTERED")
    return row_idx
