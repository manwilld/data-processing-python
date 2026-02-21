#!/bin/bash
cd /root/data-processing-python
claude -p --permission-mode dontAsk "$(cat PROMPT.md)" 2>&1 | tee /root/data-processing-python/agent.log
echo "EXIT CODE: $?" >> /root/data-processing-python/agent.log
