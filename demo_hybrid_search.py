"""
Stretch feature demo — Dense vs. BM25 vs. Hybrid (RRF) retrieval.

Runs three illustrative queries that exercise different retrieval strengths:
- A category query where dense should win (paraphrase: "ramen" ↔ "noodles").
- An exact-name query where BM25 should win (the word "Huggermugger" is
  rare and dense embeddings smear it across many cafes).
- A multi-word descriptive query where the hybrid should beat both.

Run with: python demo_hybrid_search.py
"""

from hybrid import dense_ranking, bm25_ranking, hybrid_search


QUERIES = [
    "Where can I get ramen near the CS department?",
    "Huggermugger restaurant",
    "halal late night quick lunch",
]


def show(title: str, rows: list[dict], score_field: str) -> None:
    print(f"\n  -- {title} --")
    for r in rows[:5]:
        score = r.get(score_field)
        score_str = f"{score:.4f}" if isinstance(score, (int, float)) else "—"
        print(f"    {r['name']:42s}  {score_field}={score_str}")


def main() -> None:
    for q in QUERIES:
        print("=" * 78)
        print(f"QUERY: {q}")
        print("=" * 78)
        show("Dense (cosine)", dense_ranking(q, n=5), "dense_score")
        show("BM25", bm25_ranking(q, n=5), "bm25_score")
        show("Hybrid (RRF, weight=1.0/1.0)", hybrid_search(q, k=5), "rrf_score")
        print()


if __name__ == "__main__":
    main()
