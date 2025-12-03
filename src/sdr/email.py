"""
Email service module for sending emails via SendGrid.

Provides abstraction for email sending functionality.
"""

import os
from typing import Dict
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

from sdr.config import EmailConfig, setup_ssl_certificates


class EmailService:
    """Service for sending emails via SendGrid."""
    
    def __init__(self, config: EmailConfig):
        """
        Initialize the email service.
        
        Args:
            config: Email configuration containing API key and email addresses
        """
        self.config = config
        self.client = sendgrid.SendGridAPIClient(api_key=config.api_key)
        setup_ssl_certificates()
    
    def send_plain_email(self, body: str, subject: str = "Sales email") -> Dict[str, str]:
        """
        Send a plain text email.
        
        Args:
            body: Email body content
            subject: Email subject line
            
        Returns:
            Dictionary with status information
            
        Raises:
            Exception: If email sending fails
        """
        from_email = Email(self.config.from_email)
        to_email = To(self.config.to_email)
        content = Content("text/plain", body)
        mail = Mail(from_email, to_email, subject, content).get()
        
        response = self.client.mail.send.post(request_body=mail)
        
        if response.status_code not in [200, 202]:
            raise Exception(f"Failed to send email. Status code: {response.status_code}")
        
        return {"status": "success", "status_code": response.status_code}
    
    def send_html_email(self, subject: str, html_body: str) -> Dict[str, str]:
        """
        Send an HTML email.
        
        Args:
            subject: Email subject line
            html_body: HTML email body content
            
        Returns:
            Dictionary with status information
            
        Raises:
            Exception: If email sending fails
        """
        from_email = Email(self.config.from_email)
        to_email = To(self.config.to_email)
        content = Content("text/html", html_body)
        mail = Mail(from_email, to_email, subject, content).get()
        
        response = self.client.mail.send.post(request_body=mail)
        
        if response.status_code not in [200, 202]:
            raise Exception(f"Failed to send email. Status code: {response.status_code}")
        
        return {"status": "success", "status_code": response.status_code}
    
    def send_test_email(self) -> Dict[str, str]:
        """
        Send a test email to verify configuration.
        
        Returns:
            Dictionary with status information
        """
        return self.send_plain_email(
            body="This is an important test email",
            subject="Test email"
        )

