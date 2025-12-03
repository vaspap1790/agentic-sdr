# SDR (Sales Development Representative) Agent System

A multi-agent system for generating and sending cold sales outreach emails using OpenAI Agents SDK.

## 🚀 Quick Start (3 Steps)

1. **Set up your API keys** - Copy `.env.example` to `.env` and add your keys:
   ```bash
   cp .env.example .env
   # Then edit .env and replace the placeholder values with your actual keys
   ```
   
   **Where to get keys:**
   - OpenAI: https://platform.openai.com/api-keys
   - SendGrid: https://sendgrid.com/ → Settings → API Keys → Create API Key
   - SendGrid Sender: Settings → Sender Authentication → Verify a Single Sender

2. **Install dependencies** (one command):
   ```bash
   uv sync
   ```

3. **Run it!** (one command):
   ```bash
   uv run python -m sdr.main send "Send a cold sales email addressed to Dear CEO"
   ```

That's it! The system will:
- Generate 3 email drafts (professional, engaging, concise)
- Pick the best one
- Format it with a subject and HTML
- Send it via SendGrid

**Other commands:**
```bash
# Test email configuration
uv run python -m sdr.main test-email

# Generate drafts without sending
uv run python -m sdr.main drafts
```

## Overview

This project implements an automated sales email system that uses multiple AI agents to:
1. Generate multiple email drafts with different styles (professional, engaging, concise)
2. Select the best email from the drafts
3. Format the email (add subject, convert to HTML)
4. Send the email via SendGrid

## Architecture

The project follows modern software engineering practices with a clean separation of concerns:

- **`src/sdr/config.py`**: Configuration management (environment variables, settings)
- **`src/sdr/agents.py`**: Agent definitions (different sales agent personalities)
- **`src/sdr/tools.py`**: Tool factory for creating function tools and agent-to-tool conversions
- **`src/sdr/email.py`**: Email service abstraction (SendGrid integration)
- **`src/sdr/manager.py`**: Orchestration logic (coordinates agents and tools)
- **`src/sdr/main.py`**: CLI entry point

## Design Patterns Used

1. **Factory Pattern**: `ToolFactory` creates tools from agents and functions
2. **Strategy Pattern**: Different sales agent strategies (professional, engaging, busy)
3. **Service Pattern**: `EmailService` abstracts email sending functionality
4. **Manager Pattern**: `SDRManager` orchestrates multiple agents
5. **Dependency Injection**: Configuration passed to components

## Setup

### Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/) package manager
- SendGrid account (free tier available)
- OpenAI API key

### Installation

1. **Install uv** (if not already installed):
   ```bash
   pip install uv
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and add:
   - `OPENAI_API_KEY`: Your OpenAI API key from https://platform.openai.com/api-keys
   - `SENDGRID_API_KEY`: Your SendGrid API key from https://sendgrid.com/
   - `SENDGRID_FROM_EMAIL`: Your verified sender email
   - `SENDGRID_TO_EMAIL`: Recipient email address

3. **Install dependencies**:
   ```bash
   uv sync
   ```

### SendGrid Setup

1. Create an account at https://sendgrid.com/
2. Create an API key:
   - Go to Settings > API Keys
   - Click "Create API Key"
   - Copy the key to your `.env` file
3. Verify your sender email:
   - Go to Settings > Sender Authentication
   - Click "Verify a Single Sender"
   - Verify your email address

## Usage

### CLI Commands

**Test email configuration:**
```bash
uv run python -m sdr.main test-email
```

**Send a sales email (with handoff to email manager):**
```bash
uv run python -m sdr.main send "Send a cold sales email addressed to Dear CEO"
```

**Send with tools only (no handoff):**
```bash
uv run python -m sdr.main send "Send a cold sales email" --no-handoff
```

**Generate email drafts without sending:**
```bash
uv run python -m sdr.main drafts --message "Write a cold sales email"
```

### Programmatic Usage

```python
import asyncio
from sdr import SDRManager

async def main():
    manager = SDRManager()
    
    # Send email with handoff
    result = await manager.send_sales_email(
        message="Send a cold sales email addressed to Dear CEO",
        use_handoff=True
    )
    
    # Or generate drafts only
    emails = await manager.generate_emails("Write a cold sales email")
    best = await manager.pick_best_email(emails)
    print(best)

asyncio.run(main())
```

## Agent Workflow

1. **Sales Manager Agent**: Coordinates the email generation process
   - Uses three sales agent tools to generate drafts
   - Evaluates and selects the best email
   - Handoffs to Email Manager for formatting and sending

2. **Sales Agents** (as tools):
   - Professional Sales Agent: Writes professional, serious emails
   - Engaging Sales Agent: Writes witty, engaging emails
   - Busy Sales Agent: Writes concise, to-the-point emails

3. **Email Manager Agent** (handoff):
   - Writes email subject using Subject Writer tool
   - Converts email body to HTML using HTML Converter tool
   - Sends HTML email using send_html_email tool

## Troubleshooting

### SSL Certificate Errors

If you encounter SSL certificate errors:
```bash
uv add certifi
```

The code will automatically use certifi if available.

### Email Not Received

1. Check your spam folder
2. Verify your SendGrid API key in `.env`
3. Verify your sender email in SendGrid dashboard
4. Check the trace at https://platform.openai.com/traces

### Import Errors

Make sure you're running commands from the `sdr` directory:
```bash
cd sdr
uv run python -m sdr.main test-email
```

## Project Structure

```
sdr/
├── src/
│   └── sdr/
│       ├── __init__.py          # Package initialization
│       ├── config.py            # Configuration management
│       ├── agents.py            # Agent definitions
│       ├── tools.py             # Tool factory
│       ├── email.py             # Email service
│       ├── manager.py           # Orchestration logic
│       ├── main.py              # CLI entry point
│       └── example.py           # Example usage
├── pyproject.toml              # Project configuration and dependencies
├── .env.example                # Environment variables template
├── README.md                   # This file
└── uv.lock                     # Locked dependencies (auto-generated)
```

## License

This project is part of the Agentic AI course materials.
