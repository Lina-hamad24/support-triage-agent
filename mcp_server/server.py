import sys
from pathlib import Path

# Add the project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from mcp.server.fastmcp import FastMCP

from app.tickets import create_ticket
from app.retrieval import build_vector_store


# Create MCP server
mcp = FastMCP("Support Triage Tools")


# Build the vector store once when the MCP server starts
vector_store = build_vector_store()


@mcp.tool()
def create_support_ticket(question: str) -> str:
    """Create a support ticket for a customer issue."""

    ticket_id = create_ticket(question)

    return f"Support ticket created successfully. Ticket ID: {ticket_id}"


@mcp.tool()
def search_documents(question: str) -> str:
    """Search the support documentation for information relevant to a customer question."""

    documents = vector_store.similarity_search(question, k=2)

    if not documents:
        return "No relevant documents were found."

    results = []

    for document in documents:
        results.append(document.page_content)

    return "\n\n---\n\n".join(results)


if __name__ == "__main__":
    mcp.run()