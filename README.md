# AsterSupport-AI

A privacy-aware AI customer support agent built in Python.

## Overview

AsterSupport-AI is a lightweight customer support agent designed to answer questions using a controlled knowledge base and provide safe order-status information.

The system focuses on:

- Knowledge-grounded responses
- Order-status lookup
- Multi-turn conversations
- Privacy protection
- Human handoff
- Unknown-order handling
- Prompt-injection protection
- Safe handling of unsupported questions

## Project Structure

```text
AsterSupport-AI/
│
├── data/
│   └── orders.json
│
├── knowledge-base/
│   ├── 01-returns-policy.md
│   ├── 02-shipping-policy.md
│   └── 03-product-care.md
│
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── knowledge_base.py
│   ├── models.py
│   ├── order_tool.py
│   └── retriever.py
│
├── tests/
│   └── test_agent.py
│
├── demo.py
├── requirements.txt
└── README.md
```
## Project Demo

### AI Customer Support Agent in Action

![AsterSupport-AI Demo](AsterSupport-AI-recruiter-demo(1).gif)


