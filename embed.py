"""
Milestone 4 — Embedding and retrieval.

Embeds chunks from ingest.py using all-MiniLM-L6-v2 (sentence-transformers),
stores them in a local ChromaDB collection, and exposes a retrieve() function.
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, chunk_documents

COLLECTION_NAME = "restaurants"
CHROMA_DIR = ".chroma"
EMBED_MODEL = "all-MiniLM-L6-v2"


def build_vectorstore(chunks: list[dict], persist_dir: str = CHROMA_DIR) -> chromadb.Collection:
    """Embed all chunks and store in ChromaDB. Returns the collection."""
    print(f"Loading embedding model: {EMBED_MODEL} ...")
    model = SentenceTransformer(EMBED_MODEL)

    print(f"Embedding {len(chunks)} chunks ...")
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    client = chromadb.PersistentClient(path=persist_dir)

    # delete existing collection so re-runs start fresh
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        embeddings=embeddings,
        documents=texts,
        metadatas=[{"source": c["source"]} for c in chunks],
    )

    print(f"Stored {collection.count()} chunks in ChromaDB ({persist_dir}).\n")
    return collection


def load_collection(persist_dir: str = CHROMA_DIR) -> chromadb.Collection:
    """Load an already-built ChromaDB collection from disk."""
    client = chromadb.PersistentClient(path=persist_dir)
    return client.get_collection(COLLECTION_NAME)


def retrieve(query: str, k: int = 5, persist_dir: str = CHROMA_DIR) -> list[dict]:
    """
    Return the top-k most relevant chunks for a query.
    Each result: {text, source, distance}
    """
    model = SentenceTransformer(EMBED_MODEL)
    query_vec = model.encode([query]).tolist()

    collection = load_collection(persist_dir)
    results = collection.query(
        query_embeddings=query_vec,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    hits = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        hits.append({"text": doc, "source": meta["source"], "distance": round(dist, 4)})
    return hits


def test_retrieval(queries: list[str], k: int = 5) -> None:
    """Run test queries and print results with distance scores."""
    for query in queries:
        print(f"\n{'='*60}")
        print(f"QUERY: {query}")
        print(f"{'='*60}")
        hits = retrieve(query, k=k)
        for rank, hit in enumerate(hits, 1):
            # extract restaurant name and key fields for compact display
            lines = hit["text"].split("\n")
            name_line = next((l for l in lines if l.startswith("Restaurant:")), "")
            dist_line = next((l for l in lines if l.startswith("Distance from")), "")
            cat_line  = next((l for l in lines if l.startswith("Categories:")), "")
            rat_line  = next((l for l in lines if l.startswith("Rating:")), "")
            price_line = next((l for l in lines if l.startswith("Price")), "")
            print(
                f"  [{rank}] dist={hit['distance']:.4f} | "
                f"{name_line} | {dist_line} | {cat_line} | {rat_line} | {price_line}"
            )


if __name__ == "__main__":
    # Build vector store
    docs = load_documents("documents")
    chunks = chunk_documents(docs)
    build_vectorstore(chunks)

    # Test with 3 evaluation plan queries
    test_queries = [
        "Which restaurant is closest to Siebel Center for Computer Science?",
        "What Korean restaurants are near the CS building?",
        "Which coffee shops within 0.5 miles of Siebel Center have a rating of 4.0 or higher?",
    ]
    test_retrieval(test_queries, k=5)
