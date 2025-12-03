"""
Agent definitions for the SDR system.

Contains all agent classes and their instructions.
"""

from agents import Agent
from sdr.config import AgentConfig


class SalesAgent:
    """Base class for sales agents with different writing styles."""
    
    def __init__(self, name: str, instructions: str, config: AgentConfig):
        """
        Initialize a sales agent.
        
        Args:
            name: Agent name
            instructions: Agent instructions
            config: Agent configuration
        """
        self.name = name
        self.instructions = instructions
        self.config = config
        self._agent = None
    
    @property
    def agent(self) -> Agent:
        """Get the underlying Agent instance."""
        if self._agent is None:
            self._agent = Agent(
                name=self.name,
                instructions=self.instructions,
                model=self.config.model
            )
        return self._agent


class ProfessionalSalesAgent(SalesAgent):
    """Professional, serious sales agent."""
    
    def __init__(self, config: AgentConfig):
        instructions = (
            f"You are a sales agent working for {config.company_context}. "
            "You write professional, serious cold emails."
        )
        super().__init__("Professional Sales Agent", instructions, config)


class EngagingSalesAgent(SalesAgent):
    """Humorous, engaging sales agent."""
    
    def __init__(self, config: AgentConfig):
        instructions = (
            f"You are a humorous, engaging sales agent working for {config.company_context}. "
            "You write witty, engaging cold emails that are likely to get a response."
        )
        super().__init__("Engaging Sales Agent", instructions, config)


class BusySalesAgent(SalesAgent):
    """Concise, to-the-point sales agent."""
    
    def __init__(self, config: AgentConfig):
        instructions = (
            f"You are a busy sales agent working for {config.company_context}. "
            "You write concise, to the point cold emails."
        )
        super().__init__("Busy Sales Agent", instructions, config)


class SalesPickerAgent:
    """Agent that picks the best sales email from multiple options."""
    
    def __init__(self, config: AgentConfig):
        """
        Initialize the sales picker agent.
        
        Args:
            config: Agent configuration
        """
        self.config = config
        instructions = (
            "You pick the best cold sales email from the given options. "
            "Imagine you are a customer and pick the one you are most likely to respond to. "
            "Do not give an explanation; reply with the selected email only."
        )
        self._agent = Agent(
            name="sales_picker",
            instructions=instructions,
            model=config.model
        )
    
    @property
    def agent(self) -> Agent:
        """Get the underlying Agent instance."""
        return self._agent


class SubjectWriterAgent:
    """Agent that writes email subjects."""
    
    def __init__(self, config: AgentConfig):
        """
        Initialize the subject writer agent.
        
        Args:
            config: Agent configuration
        """
        self.config = config
        instructions = (
            "You can write a subject for a cold sales email. "
            "You are given a message and you need to write a subject for an email "
            "that is likely to get a response."
        )
        self._agent = Agent(
            name="Email subject writer",
            instructions=instructions,
            model=config.model
        )
    
    @property
    def agent(self) -> Agent:
        """Get the underlying Agent instance."""
        return self._agent


class HTMLConverterAgent:
    """Agent that converts text emails to HTML."""
    
    def __init__(self, config: AgentConfig):
        """
        Initialize the HTML converter agent.
        
        Args:
            config: Agent configuration
        """
        self.config = config
        instructions = (
            "You can convert a text email body to an HTML email body. "
            "You are given a text email body which might have some markdown "
            "and you need to convert it to an HTML email body with simple, "
            "clear, compelling layout and design."
        )
        self._agent = Agent(
            name="HTML email body converter",
            instructions=instructions,
            model=config.model
        )
    
    @property
    def agent(self) -> Agent:
        """Get the underlying Agent instance."""
        return self._agent


class EmailManagerAgent:
    """Agent that manages email formatting and sending."""
    
    def __init__(self, config: AgentConfig, tools: list):
        """
        Initialize the email manager agent.
        
        Args:
            config: Agent configuration
            tools: List of tools available to the agent
        """
        self.config = config
        instructions = (
            "You are an email formatter and sender. You receive the body of an email to be sent. "
            "You first use the subject_writer tool to write a subject for the email, "
            "then use the html_converter tool to convert the body to HTML. "
            "Finally, you use the send_html_email tool to send the email with the subject and HTML body."
        )
        self._agent = Agent(
            name="Email Manager",
            instructions=instructions,
            tools=tools,
            model=config.model,
            handoff_description="Convert an email to HTML and send it"
        )
    
    @property
    def agent(self) -> Agent:
        """Get the underlying Agent instance."""
        return self._agent
