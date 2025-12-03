"""
Configuration management for the SDR system.

Handles environment variables and configuration settings.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class EmailConfig:
    """Email configuration settings."""
    api_key: str
    from_email: str
    to_email: str
    
    @classmethod
    def from_env(cls) -> "EmailConfig":
        """Load email configuration from environment variables."""
        load_dotenv(override=True)
        
        api_key = os.environ.get("SENDGRID_API_KEY")
        if not api_key:
            raise ValueError(
                "SENDGRID_API_KEY environment variable is not set. "
                "Please set it in your .env file."
            )
        
        from_email = os.environ.get("SENDGRID_FROM_EMAIL", "ed@edwarddonner.com")
        to_email = os.environ.get("SENDGRID_TO_EMAIL", "ed.donner@gmail.com")
        
        return cls(
            api_key=api_key,
            from_email=from_email,
            to_email=to_email,
        )


@dataclass
class AgentConfig:
    """Agent configuration settings."""
    model: str = "gpt-4o-mini"
    company_name: str = "ComplAI"
    company_description: str = (
        "a company that provides a SaaS tool for ensuring SOC2 compliance "
        "and preparing for audits, powered by AI"
    )
    
    @property
    def company_context(self) -> str:
        """Get the company context string for agent instructions."""
        return f"{self.company_name}, {self.company_description}"


def setup_ssl_certificates() -> None:
    """
    Setup SSL certificates for SendGrid.
    
    This is a workaround for SSL certificate issues on some systems.
    """
    try:
        import certifi
        os.environ['SSL_CERT_FILE'] = certifi.where()
    except ImportError:
        # certifi not installed, skip SSL setup
        pass

