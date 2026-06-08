"""
Stretch feature demo — chunking strategy comparison.

Builds a second ChromaDB collection using fixed-size 200-char chunks with
50-char overlap, then runs the same query set against both strategies and
shows top-5 results side by side.

Strategy A — whole-document (current production strategy in embed.py):
  100 chunks, ~640-790 chars each, one chunk per restaurant.

Strategy B — fixed-size 200-char windows with 50-char overlap:
  ~400 chunks, each ~200 chars, multiple chunks per restaurant. A single
  restaurant's metadata fields may now span multiple chunks.

Run with: python demo_chunking_comparison.py
"""

import chromadb
from sentence_transformers import SentenceTransformer

from embed import EMBED_MODEL, CHROMA_DIR, COLLECTION_NAME
from ingest import load_documents, chunk_documents_fixed


ALT_DIR = ".chroma_fixed200"
ALT_COLLECTION = "restaurants_fixed200"


def build_fixed_collection():
    """Build the alternative fixed-size collection (idempotent)."""
    docs = load_documents("documents")
    chunks = chunk_documents_fixed(docs, size=200, overlap=50)

    model = SentenceTransformer(EMBED_MODEL)
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=False).tolist()

    client = chromadb.PersistentClient(path=ALT_DIR)
    try:
        client.delete_collection(ALT_COLLECTION)
    except Exception:
        pass
    coll = client.create_collection(ALT_COLLECTION, metadata={"hnsw:space": "cosine"})
    coll.add(
        ids=[str(i) for i in range(len(chunks))],
        embeddings=embeddings,
        documents=texts,
        metadatas=[
            {
                "source": c["source"],
                "name": c.get("name", ""),
                "chunk_start": int(c.get("chunk_start", 0)),
            }
            for c in chunks
        ],
    )
    print(f"Built alt collection: {coll.count()} fixed-200char chunks "
          f"(vs. 100 whole-document chunks).\n")
    return coll


def query_collection(client_dir: str, coll_name: str, query: str, k: int = 5) -> list[dict]:
    """Run a single query against a named collection."""
    model = SentenceTransformer(EMBED_MODEL)
    query_vec = model.encode([query]).tolist()
    client = chromadb.PersistentClient(path=client_dir)
    coll = client.get_collection(coll_name)
    res = coll.query(
        query_embeddings=query_vec,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {
            "source": m["source"],
            "name": m.get("name", "?"),
            "chunk_start": m.get("chunk_start", None),
            "distance": round(d, 4),
            "snippet": doc[:80].replace("\n", " "),
        }
        for doc, m, d in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])
    ]


QUERIES = [
    "What Korean restaurants are near the CS building?",
    "Where can I get ramen near the CS department?",
    "Which coffee shops within 0.5 miles of Siebel have a rating above 4.0?",
]


def main():
    build_fixed_collection()

    for q in QUERIES:
        print("=" * 100)
        print(f"QUERY: {q}")
        print("=" * 100)

        print("\n  Strategy A — whole-document (100 chunks):")
        for h in query_collection(CHROMA_DIR, COLLECTION_NAME, q):
            print(f"    dist={h['distance']:.4f}  {h['name']:38s}")

        print("\n  Strategy B — fixed-200char windows (~400 chunks):")
        for h in query_collection(ALT_DIR, ALT_COLLECTION, q):
            tag = f"  chunk_start={h['chunk_start']}" if h["chunk_start"] is not None else ""
            print(f"    dist={h['distance']:.4f}  {h['name']:38s}{tag}")
            print(f"       text starts: {h['snippet']!r}")
        print()


if __name__ == "__main__":
    main()
