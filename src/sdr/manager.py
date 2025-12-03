"""
Sales Manager orchestration logic.

Coordinates multiple agents to generate and send sales emails.
"""

from typing import Optional
from pydantic import BaseModel
from agents import Agent, Runner, trace, input_guardrail, GuardrailFunctionOutput

from sdr.agents import (
    ProfessionalSalesAgent,
    EngagingSalesAgent,
    BusySalesAgent,
    EmailManagerAgent,
)
from sdr.tools import ToolFactory
from sdr.config import AgentConfig, EmailConfig


class NameCheckOutput(BaseModel):
    """Output model for name check guardrail."""
    is_name_in_message: bool
    name: str


class SDRManager:
    """
    Sales Development Representative Manager.
    
    Orchestrates multiple agents to generate and send cold sales emails.
    """
    
    def __init__(
        self,
        agent_config: Optional[AgentConfig] = None,
        email_config: Optional[EmailConfig] = None
    ):
        """
        Initialize the SDR Manager.
        
        Args:
            agent_config: Agent configuration (defaults to AgentConfig())
            email_config: Email configuration (defaults to EmailConfig.from_env())
        """
        self.agent_config = agent_config or AgentConfig()
        self.email_config = email_config or EmailConfig.from_env()
        
        # Initialize tool factory
        self.tool_factory = ToolFactory(self.agent_config, self.email_config)
        
        # Initialize sales agents
        self.professional_agent = ProfessionalSalesAgent(self.agent_config)
        self.engaging_agent = EngagingSalesAgent(self.agent_config)
        self.busy_agent = BusySalesAgent(self.agent_config)
        
        # Create tools
        self.sales_tools = self.tool_factory.create_sales_agent_tools()
        self.email_tool = self.tool_factory.create_email_tool()
        
        # Create email formatting tools for handoff
        email_formatting_tools = self.tool_factory.create_email_formatting_tools()
        html_email_tool = self.tool_factory.create_html_email_tool()
        email_tools = email_formatting_tools + [html_email_tool]
        
        # Initialize email manager agent
        self.email_manager = EmailManagerAgent(self.agent_config, email_tools)
        
        # Create guardrail agent
        self.guardrail_agent = self._create_guardrail_agent()
        
        # Create sales manager agent
        self.sales_manager = self._create_sales_manager()
    
    def _create_guardrail_agent(self) -> Agent:
        """
        Create the guardrail agent for name checking.
        
        Returns:
            Configured guardrail agent
        """
        return Agent(
            name="Name check",
            instructions="Check if the user is including someone's personal name in what they want you to do.",
            output_type=NameCheckOutput,
            model="gpt-4o-mini"
        )
    
    @input_guardrail
    async def guardrail_against_name(self, ctx, agent, message):
        """
        Guardrail function to check if a personal name is included in the message.
        
        Args:
            ctx: Context object
            agent: Agent instance
            message: User message
            
        Returns:
            GuardrailFunctionOutput indicating if name was found
        """
        result = await Runner.run(self.guardrail_agent, message, context=ctx.context)
        is_name_in_message = result.final_output.is_name_in_message
        return GuardrailFunctionOutput(
            output_info={"found_name": result.final_output},
            tripwire_triggered=is_name_in_message
        )
    
    def _create_sales_manager(self) -> Agent:
        """
        Create the sales manager agent with tools and handoffs.
        
        Returns:
            Configured sales manager agent
        """
        instructions = """
You are a Sales Manager at ComplAI. Your goal is to find the single best cold sales email using the sales_agent tools.
 
Follow these steps carefully:
1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
 
2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
You can use the tools multiple times if you're not satisfied with the results from the first try.
 
3. Handoff for Sending: Pass ONLY the winning email draft to the 'Email Manager' agent. The Email Manager will take care of formatting and sending.
 
Crucial Rules:
- You must use the sales agent tools to generate the drafts — do not write them yourself.
- You must hand off exactly ONE email to the Email Manager — never more than one.
"""
        
        return Agent(
            name="Sales Manager",
            instructions=instructions,
            tools=self.sales_tools,
            handoffs=[self.email_manager.agent],
            model=self.agent_config.model,
            input_guardrails=[self.guardrail_against_name]
        )
    
    async def send_sales_email(
        self,
        message: str,
        use_handoff: bool = True,
        trace_name: str = "Automated SDR"
    ):
        """
        Generate and send a sales email.
        
        Args:
            message: User message/instruction for the sales email
            use_handoff: Whether to use handoff to email manager (default: True)
                         If False, uses tools directly
            trace_name: Name for the trace (default: "Automated SDR")
            
        Returns:
            Result from the agent runner
        """
        if not use_handoff:
            # Use the simpler version with tools only
            return await self._send_with_tools(message, trace_name)
        else:
            # Use handoff to email manager
            return await self._send_with_handoff(message, trace_name)
    
    async def _send_with_tools(self, message: str, trace_name: str):
        """
        Send email using tools only (no handoff).
        
        Args:
            message: User message/instruction
            trace_name: Name for the trace
            
        Returns:
            Result from the agent runner
        """
        instructions = """
You are a Sales Manager at ComplAI. Your goal is to find the single best cold sales email using the sales_agent tools.
 
Follow these steps carefully:
1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
 
2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
 
3. Use the send_email tool to send the best email (and only the best email) to the user.
 
Crucial Rules:
- You must use the sales agent tools to generate the drafts — do not write them yourself.
- You must send ONE email using the send_email tool — never more than one.
"""
        
        sales_manager = Agent(
            name="Sales Manager",
            instructions=instructions,
            tools=self.sales_tools + [self.email_tool],
            model=self.agent_config.model,
            input_guardrails=[self.guardrail_against_name]
        )
        
        with trace(trace_name):
            result = await Runner.run(sales_manager, message)
        
        return result
    
    async def _send_with_handoff(self, message: str, trace_name: str):
        """
        Send email using handoff to email manager.
        
        Args:
            message: User message/instruction
            trace_name: Name for the trace
            
        Returns:
            Result from the agent runner
        """
        with trace(trace_name):
            result = await Runner.run(self.sales_manager, message)
        
        return result
    
    async def generate_emails(self, message: str = "Write a cold sales email"):
        """
        Generate multiple email drafts without sending.
        
        Args:
            message: User message/instruction
            
        Returns:
            List of generated email drafts
        """
        import asyncio
        
        results = await asyncio.gather(
            Runner.run(self.professional_agent.agent, message),
            Runner.run(self.engaging_agent.agent, message),
            Runner.run(self.busy_agent.agent, message),
        )
        
        return [result.final_output for result in results]
    
    async def pick_best_email(self, emails: list[str]) -> str:
        """
        Pick the best email from a list of options.
        
        Args:
            emails: List of email drafts
            
        Returns:
            The best email selected by the picker agent
        """
        from sdr.agents import SalesPickerAgent
        
        picker = SalesPickerAgent(self.agent_config)
        emails_text = "Cold sales emails:\n\n" + "\n\nEmail:\n\n".join(emails)
        
        result = await Runner.run(picker.agent, emails_text)
        return result.final_output

