"""Al-Mehdi: a human-governed AI safety research platform."""

from .catalog import build_catalog
from .orchestrator import SafetyOrchestrator

__all__ = ["SafetyOrchestrator", "build_catalog"]
__version__ = "0.2.0"
