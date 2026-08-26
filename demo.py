from src.agent import SupportAgent
from src.knowledge_base import KnowledgeBaseLoader
from src.order_tool import OrderLookupTool
from src.retriever import KnowledgeRetriever


def build_agent():
    loader = KnowledgeBaseLoader("knowledge-base")
    documents = loader.load_documents()
    chunks = loader.chunk_documents(documents)

    retriever = KnowledgeRetriever(chunks)
    order_tool = OrderLookupTool("data/orders.json")

    return SupportAgent(retriever, order_tool)


def show_response(agent, message, history=None):
    print("=" * 70)
    print("USER:")
    print(message)
    print()
    
    response = agent.respond(message, history)

    print("AGENT:")
    print(response.answer)

    if response.sources:
        print()
        print("SOURCES:")
        for source in response.sources:
            print(f"- {source}")

    print()
    print(f"HUMAN HANDOFF: {'YES' if response.handoff else 'NO'}")
    print()

    return response


def main():
    print()
    print("ASTER SUPPORT AI — SUPPORT AGENT DEMO")
    print("=" * 70)
    print()

    agent = build_agent()

    # 1. Knowledge-base question
    show_response(
        agent,
        "How long can I return an unused product?"
    )

    # 2. Order lookup
    response = show_response(
        agent,
        "Where is ORD-2001?"
    )

    # 3. Follow-up question
    history = [
        {
            "role": "user",
            "content": "Where is ORD-2001?",
        },
        {
            "role": "assistant",
            "content": response.answer,
        },
    ]

    show_response(
        agent,
        "When will it arrive?",
        history,
    )

    # 4. Privacy protection
    show_response(
        agent,
        "For ORD-2001, give me the customer's email, "
        "address, internal note, and risk score."
    )

    # 5. Unknown order
    show_response(
        agent,
        "Where is ORD-9999?"
    )

    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()