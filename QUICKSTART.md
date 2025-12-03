# Quick Start Guide

Get the SDR system running in 3 steps:

## Step 1: Set Up Environment Variables

Copy the example file and add your keys:

```bash
cd sdr
cp .env.example .env
```

Then edit `.env` and replace the placeholder values with your actual keys:

```env
OPENAI_API_KEY=sk-your-openai-key-here
SENDGRID_API_KEY=SG.your-sendgrid-key-here
SENDGRID_FROM_EMAIL=your-verified-email@example.com
SENDGRID_TO_EMAIL=recipient@example.com
```

**Where to get keys:**
- OpenAI: https://platform.openai.com/api-keys
- SendGrid: https://sendgrid.com/ → Settings → API Keys → Create API Key
- SendGrid Sender: Settings → Sender Authentication → Verify a Single Sender

## Step 2: Install Dependencies

```bash
uv sync
```

This will:
- Install Python 3.12 if needed
- Install all dependencies
- Create a virtual environment

## Step 3: Run It!

```bash
uv run python -m sdr.main send "Send a cold sales email addressed to Dear CEO"
```

The system will automatically:
1. Generate 3 different email drafts
2. Select the best one
3. Add a subject line
4. Convert to HTML
5. Send via SendGrid

Check your email inbox (and spam folder)!

## Troubleshooting

**Email not received?**
- Check spam folder
- Verify SendGrid API key is correct
- Verify sender email is verified in SendGrid dashboard
- Check trace at https://platform.openai.com/traces

**SSL errors?**
- Run: `uv add certifi`
- The code will automatically use certifi if available

**Import errors?**
- Make sure you're in the `sdr` directory
- Run `uv sync` again

## Next Steps

- Modify `src/sdr/agents.py` to customize agent personalities
- Modify `src/sdr/config.py` to change company information
- Check out `src/sdr/example.py` for programmatic usage

