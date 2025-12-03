"""
SDR (Sales Development Representative) Agent System

A multi-agent system for generating and sending cold sales outreach emails
using OpenAI Agents SDK.
"""

__version__ = "0.1.0"

from sdr.manager import SDRManager
from sdr.agents import (
    ProfessionalSalesAgent,
    EngagingSalesAgent,
    BusySalesAgent,
    SalesPickerAgent,
    EmailManagerAgent,
    SubjectWriterAgent,
    HTMLConverterAgent,
)

__all__ = [
    "SDRManager",
    "ProfessionalSalesAgent",
    "EngagingSalesAgent",
    "BusySalesAgent",
    "SalesPickerAgent",
    "EmailManagerAgent",
    "SubjectWriterAgent",
    "HTMLConverterAgent",
]

