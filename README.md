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

### AsterSupport-AI in Action

The demo video shows the complete execution of the customer-support agent from the command line.

The demonstration covers:

1. **Knowledge-Based Support**  
   The agent answers a customer question using information retrieved from the supplied knowledge base.

2. **Order Status Lookup**  
   The agent identifies an order and provides non-sensitive information such as its current status, shipping carrier, and estimated delivery date.

3. **Multi-Turn Conversation**  
   The agent understands a follow-up question such as "When will it arrive?" using the context of the previous order conversation.

4. **Privacy Protection & Human Handoff**  
   When asked for sensitive customer information such as an email address, shipping address, internal notes, or risk score, the agent refuses to disclose it and triggers a human handoff.

5. **Unknown Order Handling**  
   The agent safely handles an order that does not exist instead of inventing information.

6. **Automated Evaluation**  
   The project includes a 20-test automated evaluation suite covering retrieval, order handling, privacy, conversation context, prompt-injection protection, and safe fallback behavior.

### Demo GIF

The GIF provides a quick visual overview of the most important execution flow:

![AsterSupport-AI Demo](AsterSupport-AI-recruiter-demo(1).gif)

**Test Result:** `20 passed` ✅

![AsterSupport-AI Demo](AsterSupport-AI-recruiter-demo(1).gif)


