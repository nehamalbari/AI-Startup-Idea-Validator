"""Observability adapter for the project's existing Gemini API router.

The existing application already implements Gemini API-key fallback routing in
``app.config.llm``. This module reuses that configured routed model without
modifying any application file. Keeping one router avoids two independent
routing implementations and keeps observability isolated.
"""
from __future__ import annotations

from app.config import llm


def get_observability_model():
    """Return the existing application's Gemini fallback/router model."""
    return llm
