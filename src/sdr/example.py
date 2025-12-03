"""
Example usage of the SDR system.

This script demonstrates how to use the SDR Manager programmatically.
"""

import asyncio
from sdr import SDRManager


async def example_send_email():
    """Example: Send a sales email using handoff."""
    print("=" * 60)
    print("Example 1: Send Sales Email with Handoff")
    print("=" * 60)
    
    manager = SDRManager()
    
    result = await manager.send_sales_email(
        message="Send a cold sales email addressed to Dear CEO from Alice",
        use_handoff=True,
        trace_name="Example SDR Run"
    )
    
    print(f"\nResult: {result.final_output[:200]}...")
    print("\nCheck your email inbox (and spam folder)!")


async def example_generate_drafts():
    """Example: Generate multiple email drafts."""
    print("\n" + "=" * 60)
    print("Example 2: Generate Email Drafts")
    print("=" * 60)
    
    manager = SDRManager()
    
    emails = await manager.generate_emails("Write a cold sales email")
    
    print(f"\nGenerated {len(emails)} drafts:\n")
    for i, email in enumerate(emails, 1):
        print(f"--- Draft {i} ---")
        print(email[:150] + "...")
        print()
    
    # Pick the best one
    best = await manager.pick_best_email(emails)
    print(f"--- Best Email ---")
    print(best)


async def example_send_with_tools():
    """Example: Send email using tools only (no handoff)."""
    print("\n" + "=" * 60)
    print("Example 3: Send Email with Tools Only")
    print("=" * 60)
    
    manager = SDRManager()
    
    result = await manager.send_sales_email(
        message="Send a cold sales email addressed to 'Dear CEO'",
        use_handoff=False,
        trace_name="Example Tools Only"
    )
    
    print(f"\nResult: {result.final_output[:200]}...")
    print("\nCheck your email inbox (and spam folder)!")


async def main():
    """Run all examples."""
    print("\nSDR System Examples\n")
    
    # Uncomment the example you want to run:
    
    # await example_send_email()
    # await example_generate_drafts()
    # await example_send_with_tools()
    
    print("\nUncomment an example in example.py to run it!")


if __name__ == "__main__":
    asyncio.run(main())

