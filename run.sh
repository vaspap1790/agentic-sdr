#!/bin/bash
# Simple run script for the SDR system

# Default: send a sales email
if [ $# -eq 0 ]; then
    uv run python -m sdr.main send "Send a cold sales email addressed to Dear CEO"
else
    uv run python -m sdr.main "$@"
fi

