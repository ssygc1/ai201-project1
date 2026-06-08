"""
Stretch feature — hybrid BM25 + dense retrieval with Reciprocal Rank Fusion.

Why hybrid: dense embeddings (all-MiniLM-L6-v2) capture *semantic* similarity
("ramen" matches "noodles") but underweight exact-token signal. BM25 captures
exact-token / rare-word matches (the literal word "Cravings" or "halal") but
misses paraphrases. Combining them via RRF lets each method correct the
other's weakness, which is the standard hybrid-retrieval pattern in
production search engines (Vespa, Elasticsearch, OpenSearch).

How they're combined — Reciprocal Rank Fusion (RRF):
    RRF_score(d) = sum_{m in methods} 1 / (k_rrf + rank_m(d))

For each document d that appears in either method's ranking, sum the
reciprocal of (k_rrf + its rank) across both methods. Documents not in a
method's top-N contribute 0 from that method. k_rrf = 60 is the standard
constant from Cormack et al. (2009). RRF needs no score normalization
because it operates on ranks — dense cosine distances and BM25 scores live
on incompatible scales, so rank fusion is the cleanest combinator.

A weight is optional: `weight_dense` and `weight_bm25` scale each method's
RRF contribution. The default is 1.0 / 1.0 (balanced).
"""

import re
from functools import lru_cache

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from embed import EMBED_MODEL, load_collection
from ingest import chunk_documents, load_documents


K_RRF = 60  # standard RRF constant (Cormack et al., 2009)
TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    """Lowercase + alphanumeric tokenization. Good enough for short structured docs."""
    return TOKEN_RE.findall(text.lower())


@lru_cache(maxsize=1)
def _load_chunks_and_bm25():
    """Build chunks + BM25 index once per process (cached)."""
    docs = load_documents("documents")
    chunks = chunk_documents(docs)
    tokenized = [tokenize(c["text"]) for c in chunks]
    bm25 = BM25Okapi(tokenized)
    return chunks, bm25


@lru_cache(maxsize=1)
def _load_embed_model():
    return SentenceTransformer(EMBED_MODEL)


def dense_ranking(query: str, n: int = 20) -> list[dict]:
    """Top-n results from dense (ChromaDB cosine) retrieval, with rank attached."""
    model = _load_embed_model()
    query_vec = model.encode([query]).tolist()
    collection = load_collection()
    results = collection.query(
        query_embeddings=query_vec,
        n_results=n,
        include=["documents", "metadatas", "distances"],
    )
    out = []
    for rank, (doc, meta, dist) in enumerate(
        zip(results["documents"][0], results["metadatas"][0], results["distances"][0]),
        start=1,
    ):
        out.append({
            "source": meta["source"],
            "name": meta.get("name", ""),
            "rating": meta.get("rating", 0.0),
            "review_count": meta.get("review_count", 0),
            "distance_miles": meta.get("distance_miles", 999.0),
            "price_level": meta.get("price_level", 0),
            "text": doc,
            "dense_rank": rank,
            "dense_score": round(1 - dist, 4),  # cosine similarity
        })
    return out


def bm25_ranking(query: str, n: int = 20) -> list[dict]:
    """Top-n results from BM25, with rank attached."""
    chunks, bm25 = _load_chunks_and_bm25()
    scores = bm25.get_scores(tokenize(query))
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:n]
    out = []
    for rank, (idx, score) in enumerate(ranked, start=1):
        c = chunks[idx]
        out.append({
            "source": c["source"],
            "name": c.get("name", ""),
            "rating": c.get("rating", 0.0),
            "review_count": c.get("review_count", 0),
            "distance_miles": c.get("distance_miles", 999.0),
            "price_level": c.get("price_level", 0),
            "text": c["text"],
            "bm25_rank": rank,
            "bm25_score": round(float(score), 4),
        })
    return out


def hybrid_search(
    query: str,
    k: int = 5,
    pool_size: int = 20,
    weight_dense: float = 1.0,
    weight_bm25: float = 1.0,
) -> list[dict]:
    """
    Fuse dense and BM25 rankings via Reciprocal Rank Fusion.

    Each method contributes weight / (K_RRF + rank). Documents not in a
    method's top-`pool_size` contribute 0 from that method. Returns the top-k
    documents by combined RRF score, annotated with each method's rank.
    """
    dense_hits = {h["source"]: h for h in dense_ranking(query, n=pool_size)}
    bm25_hits = {h["source"]: h for h in bm25_ranking(query, n=pool_size)}

    fused: dict[str, dict] = {}
    for src in set(dense_hits) | set(bm25_hits):
        d = dense_hits.get(src)
        b = bm25_hits.get(src)
        score = 0.0
        if d is not None:
            score += weight_dense / (K_RRF + d["dense_rank"])
        if b is not None:
            score += weight_bm25 / (K_RRF + b["bm25_rank"])

        base = d or b
        fused[src] = {
            **base,
            "dense_rank": d["dense_rank"] if d else None,
            "dense_score": d["dense_score"] if d else None,
            "bm25_rank": b["bm25_rank"] if b else None,
            "bm25_score": b["bm25_score"] if b else None,
            "rrf_score": round(score, 6),
        }

    return sorted(fused.values(), key=lambda x: x["rrf_score"], reverse=True)[:k]
