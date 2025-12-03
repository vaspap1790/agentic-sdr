"""
Main entry point for the SDR system.

Provides CLI interface and example usage.
"""

import asyncio
import argparse
from typing import Optional

from sdr.manager import SDRManager
from sdr.config import AgentConfig, EmailConfig
from sdr.email import EmailService


async def test_email(email_config: EmailConfig):
    """Test email configuration."""
    print("Testing email configuration...")
    try:
        email_service = EmailService(email_config)
        result = email_service.send_test_email()
        print(f"✓ Test email sent successfully! Status code: {result.get('status_code')}")
        print("Please check your inbox (and spam folder) for the test email.")
    except Exception as e:
        print(f"✗ Failed to send test email: {e}")
        print("\nTroubleshooting:")
        print("1. Check your SENDGRID_API_KEY in .env file")
        print("2. Verify your sender email in SendGrid dashboard")
        print("3. Check spam folder")
        print("4. For SSL errors, run: uv pip install --upgrade certifi")


async def send_sales_email(
    message: str,
    use_handoff: bool = True,
    trace_name: Optional[str] = None
):
    """
    Send a sales email using the SDR system.
    
    Args:
        message: User message/instruction for the sales email
        use_handoff: Whether to use handoff to email manager
        trace_name: Optional trace name
    """
    print(f"Generating and sending sales email...")
    print(f"Message: {message}")
    print(f"Using handoff: {use_handoff}\n")
    
    try:
        manager = SDRManager()
        result = await manager.send_sales_email(
            message=message,
            use_handoff=use_handoff,
            trace_name=trace_name or "Automated SDR"
        )
        
        print(f"\n✓ Email process completed!")
        print(f"Final output: {result.final_output[:200]}...")
        print("\nCheck your email inbox (and spam folder) for the sent email.")
        print("View the trace at: https://platform.openai.com/traces")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        raise


async def generate_drafts(message: str = "Write a cold sales email"):
    """
    Generate multiple email drafts without sending.
    
    Args:
        message: User message/instruction
    """
    print(f"Generating email drafts...")
    print(f"Message: {message}\n")
    
    try:
        manager = SDRManager()
        emails = await manager.generate_emails(message)
        
        print(f"\nGenerated {len(emails)} email drafts:\n")
        for i, email in enumerate(emails, 1):
            print(f"--- Draft {i} ---")
            print(email)
            print()
        
        # Optionally pick the best one
        print("Picking the best email...")
        best = await manager.pick_best_email(emails)
        print(f"\n--- Best Email ---")
        print(best)
        
    except Exception as e:
        print(f"✗ Error: {e}")
        raise


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="SDR (Sales Development Representative) Agent System - "
                    "Multi-agent system for generating and sending cold sales emails"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Test email command
    test_parser = subparsers.add_parser("test-email", help="Test email configuration")
    
    # Send email command
    send_parser = subparsers.add_parser("send", help="Generate and send a sales email")
    send_parser.add_argument(
        "message",
        type=str,
        help="Message/instruction for the sales email"
    )
    send_parser.add_argument(
        "--no-handoff",
        action="store_true",
        help="Use tools instead of handoff"
    )
    send_parser.add_argument(
        "--trace-name",
        type=str,
        help="Name for the trace"
    )
    
    # Generate drafts command
    draft_parser = subparsers.add_parser("drafts", help="Generate email drafts")
    draft_parser.add_argument(
        "--message",
        type=str,
        default="Write a cold sales email",
        help="Message/instruction for the sales email"
    )
    
    # Default: send a sales email
    args = parser.parse_args()
    
    if args.command == "test-email":
        email_config = EmailConfig.from_env()
        asyncio.run(test_email(email_config))
    
    elif args.command == "send":
        asyncio.run(send_sales_email(
            message=args.message,
            use_handoff=not args.no_handoff,
            trace_name=args.trace_name
        ))
    
    elif args.command == "drafts":
        asyncio.run(generate_drafts(args.message))
    
    else:
        # Default action: send a sample sales email
        print("No command specified. Running default: sending a sales email...\n")
        asyncio.run(send_sales_email(
            message="Send a cold sales email addressed to Dear CEO",
            use_handoff=True,
            trace_name="SDR Default Run"
        ))


if __name__ == "__main__":
    main()

