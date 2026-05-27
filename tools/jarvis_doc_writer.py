# jarvis_doc_writer.py — narrow write surface to the WTS Drive Docs maintained by Jarvis.
# Owned by Jarvis (see .claude/agents/jarvis.md §Module: PM). Replaces the body of an existing
# Google Doc with new content; never creates docs (initial creation is done via the Drive MCP
# during one-time setup) and never deletes docs.
#
# Auth uses the existing shared service account with DWD impersonation — each target doc must
# already be shared with settings.GOOGLE_IMPERSONATION_EMAIL as Editor (the Drive folder share
# Steven set up satisfies this for the 5 WTS Drive docs).
#
# This module exists because the Drive MCP available to Jarvis exposes only create_file, with no
# update path for existing Google Doc bodies. The Docs API does support body replacement, so we
# wrap that here through the same service account that already writes Google Doc reports.

import logging
from typing import Optional

from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError

from tools.google_auth import get_service_account_credentials

logger = logging.getLogger(__name__)

# #note: Read+write scope for Google Docs. No Drive scope needed because we operate by file ID,
# not by Drive search — Jarvis already has the IDs hardcoded in its agent spec.
_SCOPES = ["https://www.googleapis.com/auth/documents"]


# #note: Authenticates with Google using the shared credential helper and returns a Docs API
# service client. DWD impersonation is required because the docs live in the emplicit.co
# Workspace domain.
def get_docs_service() -> Resource:
    creds = get_service_account_credentials(_SCOPES, impersonate=True)
    return build("docs", "v1", credentials=creds, cache_discovery=False)


# #note: Returns the document's body endIndex — the position one past the last character. The
# Docs API treats positions as 1-based inclusive of an implicit leading newline at index 1, so
# the body always has endIndex >= 2 even when "empty". Caller uses this to compute the delete
# range when replacing the body.
def get_doc_length(file_id: str) -> int:
    service = get_docs_service()
    try:
        doc = service.documents().get(documentId=file_id, fields="body(content(endIndex))").execute()
    except HttpError as exc:
        logger.error(f"Docs API get failed for file_id={file_id}: {exc}")
        raise
    content = doc.get("body", {}).get("content", [])
    if not content:
        return 2
    return content[-1].get("endIndex", 2)


# #note: Replaces the entire body of the doc with `text`. Performs the Docs API batchUpdate as
# two sequential requests: (1) deleteContentRange from index 1 to end-1, then (2) insertText at
# index 1. Returns None on success. Surfaces HttpError on failure so the caller (Jarvis) can
# log a clear message and add a `[ ]` to next_steps.md instead of looping on retries.
def replace_doc_body(file_id: str, text: str) -> None:
    if not text:
        raise ValueError("replace_doc_body requires non-empty text — refusing to wipe doc to nothing.")
    service = get_docs_service()
    end_index = get_doc_length(file_id)
    requests: list[dict] = []
    # The Docs body always has at least one character (an implicit newline). Only schedule the
    # delete when there is actual content to remove — endIndex > 2 means non-trivial body.
    if end_index > 2:
        requests.append(
            {
                "deleteContentRange": {
                    "range": {"startIndex": 1, "endIndex": end_index - 1}
                }
            }
        )
    requests.append({"insertText": {"location": {"index": 1}, "text": text}})
    try:
        service.documents().batchUpdate(documentId=file_id, body={"requests": requests}).execute()
    except HttpError as exc:
        logger.error(f"Docs API batchUpdate (replace_doc_body) failed for file_id={file_id}: {exc}")
        raise
    logger.info(f"Replaced body of doc {file_id} with {len(text)} chars.")


# #note: Appends `text` to the end of the doc body. Useful for log-style docs where Jarvis adds
# new entries without rewriting the whole file. Inserts at the position immediately before the
# trailing implicit newline so subsequent appends remain on new lines.
def append_to_doc(file_id: str, text: str) -> None:
    if not text:
        raise ValueError("append_to_doc requires non-empty text.")
    service = get_docs_service()
    end_index = get_doc_length(file_id)
    insertion_index = max(1, end_index - 1)
    requests = [{"insertText": {"location": {"index": insertion_index}, "text": text}}]
    try:
        service.documents().batchUpdate(documentId=file_id, body={"requests": requests}).execute()
    except HttpError as exc:
        logger.error(f"Docs API batchUpdate (append_to_doc) failed for file_id={file_id}: {exc}")
        raise
    logger.info(f"Appended {len(text)} chars to doc {file_id}.")


# #note: Returns the plain text body of the doc — useful for Jarvis to read current state before
# deciding whether a body change is actually needed (avoids no-op writes). Returns empty string
# if the doc has no body content. Optional `max_chars` truncates the return value to avoid pulling
# multi-megabyte docs into memory unnecessarily.
def read_doc_text(file_id: str, max_chars: Optional[int] = None) -> str:
    service = get_docs_service()
    try:
        doc = service.documents().get(documentId=file_id, fields="body").execute()
    except HttpError as exc:
        logger.error(f"Docs API get (read_doc_text) failed for file_id={file_id}: {exc}")
        raise
    pieces: list[str] = []
    for element in doc.get("body", {}).get("content", []):
        paragraph = element.get("paragraph")
        if not paragraph:
            continue
        for run in paragraph.get("elements", []):
            text_run = run.get("textRun")
            if text_run and "content" in text_run:
                pieces.append(text_run["content"])
    full = "".join(pieces)
    if max_chars is not None and len(full) > max_chars:
        return full[:max_chars]
    return full
