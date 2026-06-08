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


PRICE_LEVELS = {"N/A": 0, "$": 1, "$$": 2, "$$$": 3, "$$$$": 4}


def parse_metadata(text: str) -> dict:
    """
    Extract structured numeric fields from a restaurant document so they can be
    stored as ChromaDB metadata and filtered with `where` clauses.
    """
    def first(pattern, default=None, cast=str):
        m = re.search(pattern, text, re.MULTILINE)
        if not m:
            return default
        try:
            return cast(m.group(1).strip())
        except (ValueError, TypeError):
            return default

    price_raw = first(r"^Price Level:\s*(.+)$", default="N/A")
    return {
        "name": first(r"^Restaurant:\s*(.+)$", default=""),
        "rating": first(r"^Rating:\s*([\d.]+)", default=0.0, cast=float),
        "review_count": first(r"^Review Count:\s*(\d+)", default=0, cast=int),
        "distance_miles": first(r"^Distance from Siebel Center:\s*([\d.]+)", default=999.0, cast=float),
        "price_level": PRICE_LEVELS.get((price_raw or "N/A").strip(), 0),
    }


def chunk_documents(docs: list[dict]) -> list[dict]:
    """
    One chunk per document (whole-document strategy).
    Each chunk carries the cleaned text, the source filename, and structured
    metadata (rating, review_count, distance_miles, price_level) for filtering.
    """
    chunks = []
    for doc in docs:
        text = clean_document(doc["text"])
        if len(text) == 0:
            continue
        meta = parse_metadata(text)
        chunks.append({
            "text": text,
            "source": doc["source"],
            "char_count": len(text),
            **meta,
        })
    return chunks


def chunk_documents_fixed(docs: list[dict], size: int = 200, overlap: int = 50) -> list[dict]:
    """
    Alternative chunking strategy — fixed-size sliding window with overlap.
    Used only for the chunking-strategy comparison experiment. Each document
    is split into multiple chunks of `size` characters with `overlap` between
    adjacent chunks. The same per-document metadata is attached to every
    resulting chunk so downstream filtering still works.
    """
    if size <= overlap:
        raise ValueError("size must be greater than overlap")
    step = size - overlap

    chunks = []
    for doc in docs:
        text = clean_document(doc["text"])
        if len(text) == 0:
            continue
        meta = parse_metadata(text)
        for start in range(0, len(text), step):
            piece = text[start:start + size]
            if not piece.strip():
                continue
            chunks.append({
                "text": piece,
                "source": doc["source"],
                "char_count": len(piece),
                "chunk_start": start,
                **meta,
            })
            if start + size >= len(text):
                break
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
