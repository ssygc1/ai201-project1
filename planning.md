# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

The knowledge base covers restaurants within 0.5 miles of the UIUC Siebel Center for Computer Science (201 N Goodwin Ave, Urbana, IL). The target users are CS students and researchers looking for food options within walking distance of the CS building. This knowledge is valuable because there is no single authoritative source that combines distance from Siebel Center, cuisine type, price level, rating, and hours in one place — students currently have to search Yelp or Google Maps manually and mentally filter by proximity to campus. An unofficial guide scoped specifically to the CS neighborhood makes that friction disappear.

---

## Documents

All 100 documents were collected via the Yelp Fusion API on 2026-06-07 and stored as structured plain-text files in `documents/`. Each file covers one restaurant and includes address, distance from Siebel Center, cuisine categories, rating, review count, price level, phone, and opening hours. The table below lists a representative 10 of the 100 sources spanning different cuisine types and distances.

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Espresso Royale – Grainger Engineering Library | Coffee shop, 0.09 mi from Siebel | https://www.yelp.com/biz/espresso-royale-grainger-engineering-library-urbana-2 |
| 2 | Ten Second Rice Noodle | Chinese noodle shop, 0.29 mi, rated 5.0 | https://www.yelp.com/biz/ten-second-rice-noodle-champaign |
| 3 | Sushi Ichiban | Japanese sushi bar, 0.30 mi | https://www.yelp.com/biz/sushi-ichiban-champaign |
| 4 | Burrito King | Mexican food truck, 0.31 mi | https://www.yelp.com/biz/burrito-king-urbana |
| 5 | Spoon House Korean Kitchen | Korean restaurant, 0.33 mi | https://www.yelp.com/biz/spoon-house-korean-kitchen-champaign |
| 6 | Oozu Ramen Bar | Ramen, 0.34 mi, rated 4.0 | https://www.yelp.com/biz/oozu-ramen-bar-champaign |
| 7 | Susuru Ramen Bar | Ramen and Japanese curry, 0.35 mi | https://www.yelp.com/biz/susuru-ramen-bar-champaign |
| 8 | Cracked on Green | Breakfast/brunch food truck, 0.36 mi, rated 4.0, $ | https://www.yelp.com/biz/cracked-on-green-champaign |
| 9 | Thai Fusion | Thai restaurant, 0.37 mi | https://www.yelp.com/biz/thai-fusion-champaign |
| 10 | Chipotle Mexican Grill | Fast-food Mexican, 0.38 mi, $ | https://www.yelp.com/biz/chipotle-mexican-grill-champaign |
| 11 | BrewLab Coffee | Specialty coffee shop, 0.43 mi, rated 4.4 | https://www.yelp.com/biz/brewlab-coffee-champaign |
| 12 | Infinitea | Bubble tea and desserts, 0.29 mi | https://www.yelp.com/biz/infinitea-urbana |

Full source list: all 100 `.txt` files in `documents/`, each named `restaurant_<slug>.txt`.

---

## Chunking Strategy

Each restaurant document is a short structured plain-text file of approximately 640–790 characters (~160–200 tokens). Documents contain three sections: a header (title, source URL, date, reference location), a `== METADATA ==` block (restaurant name, address, distance, categories, rating, review count, price, phone, hours), and a `== USEFUL FOR ==` block (semantic tags like "Asian food", "Cheap food", "Late night").

Because each document is already self-contained and small, the best chunking strategy is **one chunk per document** — no splitting is needed. Splitting within a document would separate the restaurant's name and distance (in the header) from its rating and categories (in METADATA), making either half uninterpretable on its own. Cross-document overlap is also unnecessary because each restaurant is independent.

**Chunk size:** ~700 characters (whole document) — well under the 512-token limit of all-MiniLM-L6-v2.

**Overlap:** 0 — each restaurant document is self-contained; no information spans document boundaries.

**Reasoning:** These are structured records, not long narrative text. A query about "cheap Korean food near CS" needs the restaurant's price, category, and distance to be co-located in the same chunk. Splitting by fixed character count would break exactly those relationships. Whole-document chunks preserve the full context needed to answer any question about a single restaurant.

**Final chunk count:** 100 (one per restaurant).

---

## Retrieval Approach

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers` (local, no API key required). Chosen because it runs locally with no rate limits, produces 384-dimensional vectors suited to short structured text, and is the course-recommended baseline.

**Top-k:** 5. Retrieving 5 chunks gives the LLM enough restaurant options to compare (e.g., "which of these is cheapest?") without flooding the context window with irrelevant results. For a corpus of 100 short documents, top-5 represents a useful but not exhaustive slice.

**Production tradeoff reflection:** For a real deployment, I would evaluate two alternatives. First, `text-embedding-3-large` (OpenAI API) — it achieves higher accuracy on semantic similarity benchmarks and supports longer inputs, but introduces API latency, per-token cost, and a dependency on an external service. For a query-heavy production system, those costs add up. Second, a multilingual model like `paraphrase-multilingual-MiniLM-L12-v2` would matter if the user base includes non-English speakers (plausible for an international CS student population at UIUC), since `all-MiniLM-L6-v2` is English-only. The tradeoff is slightly lower English accuracy in exchange for multilingual coverage. For this project, local inference, no cost, and adequate accuracy on English restaurant queries make `all-MiniLM-L6-v2` the right choice.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Which restaurant is closest to Siebel Center for Computer Science? | Espresso Royale – Grainger Engineering Library, 0.09 miles away (Coffee Roasteries, Coffee & Tea; rated 4.0★) |
| 2 | What Korean restaurants are near the CS building? | At least: Spoon House Korean Kitchen (0.33 mi, 3.3★), Jipbap Taste of Korea (0.35 mi, 3.9★), Yogi Korean Restaurant (0.35 mi, 3.2★), SGD Dubu (0.41 mi, 5.0★) |
| 3 | Which coffee shops within 0.5 miles of Siebel Center have a rating of 4.0 or higher? | Espresso Royale (4.0★, 0.09 mi), Hey Bobo Cafe (4.0★, 0.32 mi), Bakelab (4.6★, 0.33 mi), Cracked on Green (4.0★, 0.36 mi), Yummy Future (4.6★, 0.36 mi), Dutch Bros Coffee (4.3★, 0.40 mi), Cotti Coffee (4.5★, 0.41 mi), BrewLab Coffee (4.4★, 0.43 mi) |
| 4 | Which cheap ($ price level) restaurants near the CS building have a Yelp rating above 4.0? | Huggermugger (5.0★, $, 0.22 mi), Cravings (4.1★, $, 0.28 mi), Paris Super Crepes (4.2★, $, 0.35 mi), Cracked on Green (4.0★, $, 0.36 mi), Latea Bubble Tea Lounge (4.1★, $, 0.36 mi) |
| 5 | Which restaurant near Siebel has the most Yelp reviews? | The system should return the restaurant with the highest review_count in the corpus — retrievable from the "Review Count" field in each document. |

---

## Anticipated Challenges

1. **Sparse price data — 52 of 100 documents have "Price Level: N/A"**: The Yelp Fusion API did not return price information for over half the corpus. Queries like "what's the cheapest ramen near CS?" will silently exclude many restaurants whose price was not collected. The LLM may confidently answer based only on the restaurants that do have price data, producing an incomplete and potentially wrong response. There is no structural fix without re-collecting the data from a source that provides price information more reliably.

2. **Semantic gap between category labels and dish names**: Documents describe cuisine at the category level (e.g., "Korean, Barbeque, Seafood") but contain no menu items. A user asking "where can I get bibimbap?" or "which places serve matcha lattes?" is querying at a specificity level the corpus cannot support. The embedding model will attempt to match the query to the closest category, but for specific dishes the match is unreliable. This is a known limitation of the knowledge base, not a pipeline bug — it should be documented as a failure case in the evaluation report.

3. **Duplicate chain restaurant entries**: The corpus contains 3 Starbucks entries, 2 Taco Bells, 2 Subways, and 2 Circle Ks (different locations of the same chain). A query about "Starbucks near CS" will retrieve chunks from all three entries, and the LLM must reconcile slightly different distances for what the user likely thinks of as one restaurant. This could produce a confusing or averaged response.

---

## Architecture

```
documents/*.txt  (100 files, one per restaurant)
       │
       ▼
┌──────────────────────────┐
│  Ingestion               │
│  os.listdir() + open()   │
│  Python stdlib           │
└────────────┬─────────────┘
             │ 100 raw document strings
             ▼
┌──────────────────────────┐
│  Chunking                │
│  1 chunk per document    │
│  ~700 chars, overlap = 0 │
│  preserve source filename│
└────────────┬─────────────┘
             │ 100 chunks + metadata
             ▼
┌──────────────────────────┐
│  Embedding               │
│  all-MiniLM-L6-v2        │
│  sentence-transformers   │
│  384-dim vectors, local  │
└────────────┬─────────────┘
             │ 100 vectors
             ▼
┌──────────────────────────┐
│  Vector Store            │
│  ChromaDB (local)        │
│  cosine similarity index │
└────────────┬─────────────┘
             │
   query ────┤ top-k = 5 nearest chunks
             ▼
┌──────────────────────────┐
│  Generation              │
│  Groq API                │
│  llama-3.3-70b-versatile │
│  grounded system prompt  │
│  + source attribution    │
└────────────┬─────────────┘
             │
             ▼
   Response text + cited restaurant names
```

---

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:**
I will give Claude this planning.md (the Chunking Strategy section) plus a sample document from `documents/` and ask it to implement `ingest.py` containing two functions: `load_documents(directory)` that reads all `.txt` files and returns a list of `{"text": ..., "source": filename}` dicts, and `chunk_documents(docs)` that returns one chunk per document (whole-document strategy, no splitting). I will verify by asserting `len(chunks) == 100` and spot-checking that chunk text matches file content.

**Milestone 4 — Embedding and retrieval:**
I will give Claude the Retrieval Approach section of this planning.md and ask it to implement `embed.py` that (1) embeds all chunks using `sentence-transformers` with `all-MiniLM-L6-v2`, (2) stores them in a local ChromaDB collection with the source filename as metadata, and (3) exposes a `retrieve(query, k=5)` function that returns the top-k chunks. I will verify by running `retrieve("ramen near CS")` and confirming that Oozu Ramen Bar and Susuru Ramen Bar appear in the top-5 results.

**Milestone 5 — Generation and interface:**
I will give Claude the grounding requirement from the project spec ("answers must be based only on the retrieved documents; include source attribution") and ask it to implement `query.py` with a `ask(query)` function that (1) calls `retrieve()`, (2) formats the chunks as numbered context blocks, (3) sends a grounded system prompt plus the context to Groq `llama-3.3-70b-versatile`, and (4) returns the response with restaurant names cited. I will verify by running all 5 evaluation questions and checking that source names appear in the output.
