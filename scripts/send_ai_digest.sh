#!/bin/bash
# AI Daily Digest Sender Script

# Generate digest and send via message tool
DIGEST=$(python3 /root/clawd/scripts/ai_daily_digest.py 2>/dev/null)

if [ -n "$DIGEST" ]; then
    /usr/bin/clawdbot message send --channel feishu --target ou_ee0dd9cd6eed23421754aa3211378657 --message "$DIGEST"
else
    echo "Failed to generate AI digest"
    exit 1
fi
