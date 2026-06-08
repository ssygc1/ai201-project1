"""
Milestone 5 — Grounded generation with source attribution.

Retrieves top-k chunks from ChromaDB, then calls Groq llama-3.3-70b-versatile
with a strict grounding prompt. Returns the answer and a list of cited sources.
"""

import os
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
    sources = [h["source"].replace("restaurant_", "").replace(".txt", "").replace("_", " ").title()
               for h in hits]

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
        print(f"\nSources retrieved: {', '.join(result['sources'])}")
