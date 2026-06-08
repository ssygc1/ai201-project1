"""
Stretch feature demo — metadata filtering vs. pure semantic retrieval.

Runs the four evaluation questions that the pure-semantic pipeline failed
on (Q1, Q3, Q4, Q5) and shows the before/after when ChromaDB metadata
filtering is applied. The visible effect: filtered results match the
expected answers in planning.md, while the unfiltered baseline does not.

Run with: python demo_metadata_filter.py
"""

from embed import retrieve, metadata_query


def show(rows: list[dict], fields: tuple[str, ...]) -> None:
    for r in rows:
        cells = " | ".join(f"{f}={r.get(f)}" for f in fields)
        print(f"  {r['name']:42s} | {cells}")


def section(title: str) -> None:
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


def main() -> None:
    section("Q1 — Which restaurant is closest to Siebel Center?")
    print("\n[BEFORE] semantic retrieve('closest restaurant to Siebel') top-5:")
    show(retrieve("closest restaurant to Siebel", k=5), ("distance_miles", "rating"))
    print("\n[AFTER] metadata_query(order_by='distance_miles', descending=False) top-5:")
    show(metadata_query(order_by="distance_miles", descending=False, limit=5),
         ("distance_miles", "rating"))

    section("Q3 — Coffee shops within 0.5 miles with rating >= 4.0")
    print("\n[BEFORE] semantic retrieve('coffee shops near Siebel') top-5:")
    show(retrieve("coffee shops near Siebel", k=5), ("rating", "distance_miles"))
    print("\n[AFTER] same query with where={'rating': {'$gte': 4.0}}:")
    show(retrieve("coffee shops near Siebel", k=5, where={"rating": {"$gte": 4.0}}),
         ("rating", "distance_miles"))

    section("Q4 — Cheap ($) restaurants near CS with rating > 4.0")
    print("\n[BEFORE] semantic retrieve('cheap restaurants near CS') top-5:")
    show(retrieve("cheap restaurants near CS", k=5), ("price_level", "rating"))
    print("\n[AFTER] metadata_query(where={price_level=1, rating>4.0}):")
    show(metadata_query(
            where={"$and": [{"price_level": {"$eq": 1}}, {"rating": {"$gt": 4.0}}]},
            order_by="rating", limit=5),
         ("price_level", "rating"))

    section("Q5 — Restaurant with the most Yelp reviews")
    print("\n[BEFORE] semantic retrieve('most yelp reviews near Siebel') top-5:")
    show(retrieve("most yelp reviews near Siebel", k=5), ("review_count", "rating"))
    print("\n[AFTER] metadata_query(order_by='review_count') top-5:")
    show(metadata_query(order_by="review_count", limit=5), ("review_count", "rating"))


if __name__ == "__main__":
    main()
