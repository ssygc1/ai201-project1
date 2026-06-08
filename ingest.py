"""
Milestone 3 — Document ingestion and chunking.

Strategy (from planning.md):
- One chunk per restaurant document (whole-document chunks)
- ~700 chars each, no overlap
- Source filename attached as metadata
"""

import os
import re


DOCUMENTS_DIR = "documents"


def load_documents(directory: str) -> list[dict]:
    """Read all restaurant .txt files; return list of {text, source} dicts."""
    docs = []
    for filename in sorted(os.listdir(directory)):
        if not filename.startswith("restaurant_") or not filename.endswith(".txt"):
            continue
        filepath = os.path.join(directory, filename)
        with open(filepath, encoding="utf-8") as f:
            raw = f.read()
        docs.append({"text": raw, "source": filename})
    return docs


def clean_document(text: str) -> str:
    """
    Light cleaning for structured plain-text restaurant files.
    These have no HTML, so cleaning is minimal:
    - Normalize line endings
    - Collapse multiple blank lines to one
    - Strip trailing whitespace per line
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    # collapse 3+ consecutive blank lines into 2
    cleaned = re.sub(r"\n{3,}", "\n\n", "\n".join(lines))
    return cleaned.strip()


def chunk_documents(docs: list[dict]) -> list[dict]:
    """
    One chunk per document (whole-document strategy).
    Each chunk carries the cleaned text and the source filename as metadata.
    Returns list of {text, source, char_count} dicts.
    """
    chunks = []
    for doc in docs:
        text = clean_document(doc["text"])
        if len(text) == 0:
            continue
        chunks.append({
            "text": text,
            "source": doc["source"],
            "char_count": len(text),
        })
    return chunks


def inspect_chunks(chunks: list[dict], n: int = 5) -> None:
    """Print n representative chunks for manual inspection."""
    step = max(1, len(chunks) // n)
    samples = [chunks[i] for i in range(0, len(chunks), step)][:n]

    print(f"{'='*60}")
    print(f"CHUNK INSPECTION — {n} samples (of {len(chunks)} total)")
    print(f"{'='*60}\n")

    for i, chunk in enumerate(samples, 1):
        print(f"--- Chunk {i} | source: {chunk['source']} | {chunk['char_count']} chars ---")
        print(chunk["text"])
        print()

    char_counts = [c["char_count"] for c in chunks]
    print(f"{'='*60}")
    print(f"Total chunks : {len(chunks)}")
    print(f"Char count   : min={min(char_counts)}, max={max(char_counts)}, avg={sum(char_counts)//len(char_counts)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    print("Loading documents...")
    docs = load_documents(DOCUMENTS_DIR)
    print(f"  Loaded {len(docs)} documents.\n")

    print("Chunking...")
    chunks = chunk_documents(docs)

    inspect_chunks(chunks, n=5)
