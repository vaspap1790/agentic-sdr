"""
Tool definitions for the SDR system.

Contains function tools and agent-to-tool conversions.
"""

from typing import Dict
from agents import function_tool

from sdr.agents import (
    ProfessionalSalesAgent,
    EngagingSalesAgent,
    BusySalesAgent,
    SubjectWriterAgent,
    HTMLConverterAgent,
)
from sdr.email import EmailService
from sdr.config import AgentConfig, EmailConfig


class ToolFactory:
    """Factory for creating tools from agents and functions."""
    
    def __init__(self, agent_config: AgentConfig, email_config: EmailConfig):
        """
        Initialize the tool factory.
        
        Args:
            agent_config: Agent configuration
            email_config: Email configuration
        """
        self.agent_config = agent_config
        self.email_service = EmailService(email_config)
        
        # Initialize agents
        self.professional_agent = ProfessionalSalesAgent(agent_config)
        self.engaging_agent = EngagingSalesAgent(agent_config)
        self.busy_agent = BusySalesAgent(agent_config)
        self.subject_writer = SubjectWriterAgent(agent_config)
        self.html_converter = HTMLConverterAgent(agent_config)
    
    def create_email_tool(self):
        """
        Create the send_email function tool.
        
        Returns:
            Function tool for sending plain text emails
        """
        @function_tool
        def send_email(body: str) -> Dict[str, str]:
            """Send out an email with the given body to all sales prospects."""
            return self.email_service.send_plain_email(body)
        
        return send_email
    
    def create_html_email_tool(self):
        """
        Create the send_html_email function tool.
        
        Returns:
            Function tool for sending HTML emails
        """
        @function_tool
        def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
            """Send out an email with the given subject and HTML body to all sales prospects."""
            return self.email_service.send_html_email(subject, html_body)
        
        return send_html_email
    
    def create_sales_agent_tools(self):
        """
        Create tools from the three sales agents.
        
        Returns:
            List of three agent tools
        """
        description = "Write a cold sales email"
        
        tool1 = self.professional_agent.agent.as_tool(
            tool_name="sales_agent1",
            tool_description=description
        )
        tool2 = self.engaging_agent.agent.as_tool(
            tool_name="sales_agent2",
            tool_description=description
        )
        tool3 = self.busy_agent.agent.as_tool(
            tool_name="sales_agent3",
            tool_description=description
        )
        
        return [tool1, tool2, tool3]
    
    def create_email_formatting_tools(self):
        """
        Create tools for email formatting (subject writer and HTML converter).
        
        Returns:
            List of formatting tools
        """
        subject_tool = self.subject_writer.agent.as_tool(
            tool_name="subject_writer",
            tool_description="Write a subject for a cold sales email"
        )
        
        html_tool = self.html_converter.agent.as_tool(
            tool_name="html_converter",
            tool_description="Convert a text email body to an HTML email body"
        )
        
        return [subject_tool, html_tool]

