"""
Milestone 5 — Grounded generation with source attribution.

Retrieves top-k chunks from ChromaDB, then calls Groq llama-3.3-70b-versatile
with a strict grounding prompt. Returns the answer and a list of cited sources.
"""

import os
import re
from groq import Groq
from dotenv import load_dotenv
from embed import retrieve

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"
TOP_K = 5

SYSTEM_PROMPT = """You are a restaurant guide assistant for students at the UIUC Siebel Center for Computer Science.

RULES — follow these strictly:
1. Answer ONLY using information from the documents provided below. Do not use any outside knowledge.
2. If the provided documents do not contain enough information to answer the question, respond with exactly: "I don't have enough information in my knowledge base to answer that."
3. Always cite the restaurant name(s) from the documents you used to form your answer.
4. Be specific: include distances, ratings, prices, and categories when they appear in the documents.
5. Never invent details not present in the documents."""


def format_context(hits: list[dict]) -> str:
    """Format retrieved chunks as numbered context blocks for the prompt."""
    blocks = []
    for i, hit in enumerate(hits, 1):
        blocks.append(f"[Document {i} — {hit['source']}]\n{hit['text']}")
    return "\n\n".join(blocks)


def extract_citation(chunk: dict) -> dict:
    """Pull restaurant name and Yelp URL out of a chunk's raw text."""
    text = chunk["text"]
    name_m = re.search(r"^Restaurant:\s*(.+)$", text, re.MULTILINE)
    url_m = re.search(r"^Source URL:\s*(\S+)", text, re.MULTILINE)
    fallback_name = chunk["source"].replace("restaurant_", "").replace(".txt", "").replace("_", " ").title()
    return {
        "name": name_m.group(1).strip() if name_m else fallback_name,
        "url": url_m.group(1).strip() if url_m else "",
        "source": chunk["source"],
    }


def ask(question: str, k: int = TOP_K) -> dict:
    """
    End-to-end RAG query.
    Returns {"answer": str, "sources": [str], "chunks": [dict]}
    """
    hits = retrieve(question, k=k)

    context = format_context(hits)
    user_message = f"""Documents:
{context}

Question: {question}

Answer using only the documents above. Cite restaurant names in your response."""

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.1,
        max_tokens=512,
    )

    answer = response.choices[0].message.content.strip()

    # programmatically append sources so attribution is guaranteed
    sources = [extract_citation(h) for h in hits]

    return {"answer": answer, "sources": sources, "chunks": hits}


def ask_with_history(question: str, history: list[tuple[str, str]], k: int = TOP_K) -> dict:
    """
    Multi-turn RAG query. `history` is a list of (user_msg, assistant_msg)
    tuples from prior turns. Retrieval is run over the last user question
    concatenated with the current one — this lets follow-ups like
    "which of those is the cheapest?" still pull the same topical
    documents that grounded the previous answer. The full chat history is
    also injected into the Groq messages list so the LLM can resolve
    pronouns ("those", "the second one") against earlier turns.
    """
    prior_qs = [u for u, _ in history[-2:] if u]
    retrieval_query = " ".join(prior_qs + [question]).strip()
    hits = retrieve(retrieval_query, k=k)
    context = format_context(hits)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})

    messages.append({
        "role": "user",
        "content": (
            f"Documents:\n{context}\n\n"
            f"Question: {question}\n\n"
            "Answer using only the documents above. Cite restaurant names "
            "in your response. If the question refers to a prior turn "
            "(\"those\", \"the second one\", \"that place\"), resolve the "
            "reference using the earlier messages in this conversation."
        ),
    })

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.1,
        max_tokens=512,
    )
    answer = response.choices[0].message.content.strip()
    sources = [extract_citation(h) for h in hits]
    return {"answer": answer, "sources": sources, "chunks": hits}


if __name__ == "__main__":
    test_questions = [
        # Eval Q1
        "Which restaurant is closest to Siebel Center for Computer Science?",
        # Eval Q2
        "What Korean restaurants are near the CS building?",
        # Eval Q3
        "Which coffee shops within 0.5 miles of Siebel Center have a rating of 4.0 or higher?",
        # Eval Q4
        "Which cheap ($ price level) restaurants near the CS building have a Yelp rating above 4.0?",
        # Eval Q5
        "Which restaurant near Siebel has the most Yelp reviews?",
        # Out-of-scope
        "Which professor teaches CS 447 at UIUC?",
    ]

    for q in test_questions:
        
        print(f"\n{'='*70}")
        print(f"Q: {q}")
        print(f"{'='*70}")
        result = ask(q)
        print(f"A: {result['answer']}")
        print("\nSources retrieved:")
        for s in result["sources"]:
            print(f"  - {s['name']} — {s['url']}")
