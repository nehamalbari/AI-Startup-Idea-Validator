"""DeepAgents-based metrics, quality, tracing, and safety package.

The public interface exposes only ``run_observability``.
"""
from .agent import run_observability

__all__ = ["run_observability"]
