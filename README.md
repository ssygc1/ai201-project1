# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

**UIUC CS Nearby Restaurant Guide** — restaurants within 0.5 miles of the Siebel Center for Computer Science (201 N Goodwin Ave, Urbana, IL).

CS students constantly need to answer the question "where should I eat near the CS building?" Official university resources list on-campus dining halls but not the surrounding Campustown restaurants. Yelp and Google Maps require manually filtering by distance, cuisine, price, and hours with no reference point tied to Siebel Center. This system makes that knowledge instantly searchable: a student can ask "cheap Korean food near the CS building" or "coffee shops open late near Siebel" and get a grounded, attributed answer in seconds.

---

## Document Sources

100 restaurant profiles collected from Yelp via the Yelp Fusion API on 2026-06-08. Each document is a plain-text file in `documents/` covering one restaurant within 0.5 miles of Siebel Center. Fields per document: restaurant name, address, distance from Siebel Center, cuisine categories, rating (out of 5), review count, price level, phone, and opening hours.

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Espresso Royale – Grainger Engineering Library | Coffee shop (0.09 mi) | `documents/restaurant_espresso_royale_grainger_engineering_library.txt` — https://www.yelp.com/biz/espresso-royale-grainger-engineering-library-urbana-2 |
| 2 | Ten Second Rice Noodle | Chinese noodles (0.29 mi, ★5.0) | `documents/restaurant_ten_second_rice_noodle.txt` — https://www.yelp.com/biz/ten-second-rice-noodle-champaign |
| 3 | Sushi Ichiban | Japanese sushi (0.30 mi) | `documents/restaurant_sushi_ichiban.txt` — https://www.yelp.com/biz/sushi-ichiban-champaign |
| 4 | Burrito King | Mexican food truck (0.31 mi) | `documents/restaurant_burrito_king.txt` — https://www.yelp.com/biz/burrito-king-urbana |
| 5 | Spoon House Korean Kitchen | Korean (0.33 mi, $$) | `documents/restaurant_spoon_house_korean_kitchen.txt` — https://www.yelp.com/biz/spoon-house-korean-kitchen-champaign |
| 6 | Oozu Ramen Bar | Ramen (0.34 mi, ★4.0) | `documents/restaurant_oozu_ramen_bar.txt` — https://www.yelp.com/biz/oozu-ramen-bar-champaign |
| 7 | Susuru Ramen Bar | Ramen & Japanese curry (0.35 mi) | `documents/restaurant_susuru_ramen_bar.txt` — https://www.yelp.com/biz/susuru-ramen-bar-champaign |
| 8 | Cracked on Green | Breakfast/brunch food truck (0.36 mi, ★4.0, $) | `documents/restaurant_cracked_on_green.txt` — https://www.yelp.com/biz/cracked-on-green-champaign |
| 9 | Thai Fusion | Thai (0.37 mi) | `documents/restaurant_thai_fusion.txt` — https://www.yelp.com/biz/thai-fusion-champaign |
| 10 | Chipotle Mexican Grill | Fast-food Mexican (0.38 mi, $) | `documents/restaurant_chipotle_mexican_grill.txt` — https://www.yelp.com/biz/chipotle-mexican-grill-champaign |
| 11 | BrewLab Coffee | Specialty coffee (0.43 mi, ★4.4) | `documents/restaurant_brewlab_coffee.txt` — https://www.yelp.com/biz/brewlab-coffee-champaign |
| 12 | Infinitea | Bubble tea & desserts (0.29 mi) | `documents/restaurant_infinitea.txt` — https://www.yelp.com/biz/infinitea-urbana |

Full corpus: 100 files in `documents/`, all named `restaurant_<slug>.txt`.

---

## Chunking Strategy


| # | Source document | Chunk excerpt |
|---|----------------|---------------|
| 1 | `restaurant_espresso_royale_grainger_engineering_library.txt` | `Restaurant: Espresso Royale – Grainger Engineering Library / Distance from Siebel Center: 0.09 miles / Categories: Coffee Roasteries, Coffee & Tea / Rating: 4.0 / 5.0 / Price Level: N/A` |
| 2 | `restaurant_oozu_ramen_bar.txt` | `Restaurant: Oozu Ramen Bar / Distance: 0.34 miles / Categories: Ramen / Rating: 4.0 / 5.0 / Price Level: $$ / Opening Hours: Mon: 11:30-22:00 ... / USEFUL FOR: Cheap food, Asian food, Late night` |
| 3 | `restaurant_jipbap_taste_of_korea.txt` | `Restaurant: Jipbap Taste of Korea / Distance: 0.35 miles / Categories: Korean / Rating: 3.9 / 5.0 / Price Level: $ / USEFUL FOR: Cheap food, Asian food, Takeout / delivery` |
| 4 | `restaurant_brewlab_coffee.txt` | `Restaurant: BrewLab Coffee / Distance: 0.43 miles / Categories: Coffee & Tea / Rating: 4.4 / 5.0 / Price Level: $$ / USEFUL FOR: Highly rated, Coffee / cafe, Takeout / delivery` |
| 5 | `restaurant_cracked_on_green.txt` | `Restaurant: Cracked on Green / Distance: 0.36 miles / Categories: Coffee & Tea, Breakfast & Brunch, Food Trucks / Rating: 4.0 / 5.0 / Price Level: $ / USEFUL FOR: Cheap food, Highly rated, Breakfast / brunch, Late night` |

---

## Retrieval Test Examples

The following three queries were issued directly against `retrieve(query, k=5)` in `embed.py` — these are raw retrieval results, before generation. Each row shows the top-5 chunks returned by cosine similarity over `all-MiniLM-L6-v2` embeddings, with their cosine distance, restaurant name, distance from Siebel, categories, rating, and price level.

**Query 1 — "What Korean restaurants are near the CS building?"**

| Rank | Distance | Restaurant | From Siebel | Categories | Rating | Price |
|------|----------|------------|-------------|------------|--------|-------|
| 1 | 0.3366 | Yogi Korean Restaurant | 0.35 mi | Korean | 3.2 | N/A |
| 2 | 0.3449 | Jipbap Taste of Korea | 0.35 mi | Korean | 3.9 | $$ |
| 3 | 0.3725 | Spoon House Korean Kitchen | 0.33 mi | Korean | 3.3 | $$$ |
| 4 | 0.4278 | SGD Du Bu | 0.42 mi | Korean, Food | 4.0 | N/A |
| 5 | 0.4511 | Nanjing Bistro | 0.42 mi | Chinese | 3.0 | N/A |

*Why these chunks are relevant:* The top 4 results are all explicitly tagged `Categories: Korean` — the embedding model picked up the strong category-level signal from the query word "Korean." The 5th result (Nanjing Bistro) is Chinese, not Korean, and represents a degradation as cosine distance increases past ~0.43 — the model is reaching for any Asian-cuisine document when the corpus runs out of Korean ones. This is acceptable behavior for top-k retrieval and the LLM correctly ignores it in generation.

**Query 2 — "Where can I get ramen near the CS department?"**

| Rank | Distance | Restaurant | From Siebel | Categories | Rating | Price |
|------|----------|------------|-------------|------------|--------|-------|
| 1 | 0.3617 | Susuru Ramen Bar | 0.35 mi | Ramen, Japanese Curry | 3.5 | N/A |
| 2 | 0.3965 | Oozu Ramen Bar | 0.34 mi | Ramen | 4.0 | $$$ |
| 3 | 0.5469 | Noodles and Company | 0.38 mi | Noodles, Salad, Pasta Shops | 2.9 | $$ |
| 4 | 0.5485 | Kajiken | 0.36 mi | Ramen, Desserts, Salad | 4.1 | N/A |
| 5 | 0.5611 | Spicy Tang | 0.37 mi | Chinese | 2.5 | $$$ |

*Why these chunks are relevant:* Ranks 1, 2, and 4 are exact category matches (`Ramen`) — Susuru, Oozu, and Kajiken are the three ramen shops in the corpus and all three appear in the top-5. Rank 3 (Noodles and Company) is a noodle restaurant — the embedding model treats "ramen" and "noodles" as semantically adjacent, which is reasonable given the corpus has no menu items to distinguish them. Rank 5 (Spicy Tang) is a weaker match driven by general Asian-cuisine proximity. Note the clear distance gap between the two true ramen results (~0.36–0.40) and the rest (>0.55) — this gap is a useful signal that retrieval confidence drops sharply after the obvious matches.

**Query 3 — "Which coffee shops within 0.5 miles of Siebel have a rating above 4.0?"**

| Rank | Distance | Restaurant | From Siebel | Categories | Rating | Price |
|------|----------|------------|-------------|------------|--------|-------|
| 1 | 0.3314 | BrewLab Coffee | 0.43 mi | Coffee & Tea | 4.4 | $$$ |
| 2 | 0.3400 | Starbucks | 0.23 mi | Coffee & Tea | 0.0 | N/A |
| 3 | 0.3486 | STARBUCKS | 0.44 mi | Coffee & Tea | 2.0 | $$$ |
| 4 | 0.3607 | Dutch Bros Coffee | 0.40 mi | Coffee & Tea, Juice Bars & Smoothies | 4.3 | N/A |
| 5 | 0.3711 | Cotti Coffee | 0.41 mi | Coffee & Tea | 4.5 | $$$ |

*Why these chunks are (partially) relevant:* All 5 results are tagged `Coffee & Tea` — the category-level retrieval works. But the query has *two* constraints: (a) it's a coffee shop, and (b) rating > 4.0. Pure semantic retrieval cannot enforce the numeric filter, so two of the top-5 (Starbucks at 0.0★ and STARBUCKS at 2.0★) violate the rating criterion. The LLM is left to do the filtering, and high-rated coffee shops that exist in the corpus (Bakelab 4.6, Yummy Future 4.6, Hey Bobo 4.0, Cracked on Green 4.0, Espresso Royale 4.0) never make the top-5 because they aren't more semantically similar to "coffee shops" than the Starbucks entries are. This is exactly the failure mode documented in *Failure Case Analysis* below — semantic search cannot filter on numeric metadata.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers` (local inference, no API key, 384-dimensional vectors, 512-token context limit).

**Production tradeoff reflection:** For real deployment I would weigh two alternatives. First, `text-embedding-3-large` (OpenAI API) scores higher on semantic similarity benchmarks and accepts longer inputs, but introduces per-token cost, API latency, and an external dependency — meaningful for a query-heavy system. Second, a multilingual model like `paraphrase-multilingual-MiniLM-L12-v2` would serve UIUC's international student population better, since `all-MiniLM-L6-v2` is English-only; the tradeoff is slightly lower English accuracy. For this project, local inference, zero cost, and adequate accuracy on short English restaurant records make `all-MiniLM-L6-v2` the right choice.

---

## Grounded Generation

**System prompt grounding instruction:**

The system prompt passed to `llama-3.3-70b-versatile` contains these explicit rules:

```
RULES — follow these strictly:
1. Answer ONLY using information from the documents provided below. Do not use any outside knowledge.
2. If the provided documents do not contain enough information to answer the question,
   respond with exactly: "I don't have enough information in my knowledge base to answer that."
3. Always cite the restaurant name(s) from the documents you used to form your answer.
4. Be specific: include distances, ratings, prices, and categories when they appear in the documents.
5. Never invent details not present in the documents.
```

Each retrieved chunk is wrapped in a labeled block (`[Document 1 — restaurant_foo.txt]`) so the model can identify sources. The user turn ends with: *"Answer using only the documents above. Cite restaurant names in your response."*

**How source attribution is surfaced in the response:** Attribution is enforced at two levels. The LLM is instructed to cite restaurant names inline in its answer (e.g., "According to the documents, BrewLab Coffee has a rating of 4.4…"). Additionally, `query.py` programmatically appends the list of retrieved source filenames to every response — so even if the model forgets to cite, the source list is always present in the output.

**Example response with attribution (Q2 — Korean restaurants):**

> *"The Korean restaurants near the Siebel Center for Computer Science (CS building) are Yogi Korean Restaurant, Jipbap Taste of Korea, Spoon House Korean Kitchen, and SGD Du Bu. All of these restaurants are within a short distance from the CS building, with Yogi Korean Restaurant and Jipbap Taste of Korea being 0.35 miles away, Spoon House Korean Kitchen being 0.33 miles away, and SGD Du Bu being 0.42 miles away."*
>
> Sources retrieved: Yogi Korean Restaurant, Jipbap Taste Of Korea, Spoon House Korean Kitchen, Sgd Du Bu, Nanjing Bistro

**Example response with attribution (Q3 — coffee shops 4.0+):**

> *"Based on the provided documents, the coffee shop within 0.5 miles of Siebel Center with a rating of 4.0 or higher is BrewLab Coffee, with a rating of 4.4 / 5.0, located 0.43 miles away from the Siebel Center."*
>
> Sources retrieved: Starbucks, Brewlab Coffee, Starbucks 2, Etc Coffeehouse, Starbucks 1

**Out-of-scope query refusal:**

Query: *"Which professor teaches CS 447 at UIUC?"*

> *"I don't have enough information in my knowledge base to answer that."*

The system correctly refused rather than hallucinating from training knowledge.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which restaurant is closest to Siebel Center? | Espresso Royale – Grainger Engineering Library (0.09 mi) | "Circle K, 0.28 miles away" — correctly identified the closest among retrieved docs, but Espresso Royale was never retrieved | Off-target | Inaccurate |
| 2 | What Korean restaurants are near the CS building? | Spoon House (0.33 mi), Jipbap (0.35 mi), Yogi Korean (0.35 mi), SGD Dubu (0.41 mi), SGD Du Bu (0.42 mi) | Named all 4 Korean restaurants in top-5 (Yogi, Jipbap, Spoon House, SGD Du Bu) with correct distances | Relevant | Accurate |
| 3 | Which coffee shops near Siebel have a rating of 4.0 or higher? | BrewLab (4.4★), Bakelab (4.6★), Yummy Future (4.6★), Dutch Bros (4.3★), Cotti Coffee (4.5★), Cracked on Green (4.0★), Hey Bobo (4.0★), Espresso Royale (4.0★) | Named only BrewLab Coffee (4.4★) — correctly applied the rating filter but retrieval returned mostly Starbucks entries instead of high-rated coffee shops | Partially relevant | Partially accurate |
| 4 | Which cheap ($) restaurants near CS have a Yelp rating above 4.0? | Huggermugger (5.0★, $), Cravings (4.1★, $), Paris Super Crepes (4.2★, $), Cracked on Green (4.0★, $), Latea (4.1★, $) | "I don't have enough information" — retrieval returned Circle K, Far East, Murphy's Pub, Sbarro, Evo Cafe (none matching both criteria) | Off-target | Inaccurate |
| 5 | Which restaurant near Siebel has the most Yelp reviews? | Cravings (217 reviews) | "Legends has the most reviews with 114" — Cravings was not retrieved; LLM correctly identified the maximum among retrieved docs | Off-target | Inaccurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

**Summary:** 1 accurate, 1 partially accurate, 3 inaccurate. The two failures tied to numeric fields (closest, most reviews) and the compound filter failure (cheap AND highly rated) share a root cause — semantic search cannot sort or filter by numeric values.

---

## Failure Case Analysis

**Question that failed:** "Which restaurant near Siebel has the most Yelp reviews?" (Q5)

**What the system returned:** "Legends has the most Yelp reviews with a review count of 114." The correct answer is Cravings with 217 reviews.

**Root cause (tied to a specific pipeline stage — Retrieval):** The failure is in the retrieval stage. The query "most Yelp reviews" has no strong semantic signal that maps to any particular restaurant's text. All 100 documents contain the phrase "Review Count" — the embedding for this query effectively matches against all documents equally, returning whichever five happen to score slightly higher on surface-level similarity. Cravings (the true answer) was not in the top-5 retrieved chunks. The LLM then correctly reported the maximum review count *among the retrieved documents*, which happened to be Legends (114). This is correct behavior given bad input — the bug is upstream in retrieval, not generation.

The same root cause affects Q1 (closest restaurant) and Q4 (cheap + highly rated): semantic search cannot sort or intersect on numeric metadata fields. These queries require a structured filter (e.g., `WHERE review_count = MAX(review_count)`) that pure vector similarity cannot provide.

**What you would change to fix it:** Add a metadata filtering layer using ChromaDB's `where` clause. ChromaDB supports structured filters on stored metadata fields; if `review_count` and `price_level` were stored as numeric/string metadata rather than embedded in the document text, queries like "most reviews" or "price=$" could be answered by filtering first and then re-ranking. Alternatively, a hybrid retrieval strategy (dense retrieval + BM25 keyword search) would help numeric-field queries that don't have strong semantic embeddings.

---

## Stretch Feature — Conversational Memory

**What was added:** `query.ask_with_history(question, history)` accepts a list of `(user, assistant)` tuples from prior turns and (a) concatenates the last 1–2 prior user questions with the current question to form the **retrieval** query so follow-ups still pull topically relevant documents, and (b) injects the full chat history into the Groq messages list so the LLM can **resolve referring expressions** ("those", "that one", "the second one") against earlier turns. The Gradio app exposes this as a second tab — **Chat (conversational memory)** — using `gr.Chatbot` with the standard messages format.

**Demo transcript — 3-turn exchange:**

> **Turn 1 — User:** *What Korean restaurants are near the CS building?*
>
> **Assistant:** There are several Korean restaurants near the Siebel Center for Computer Science (CS) building. These include **Yogi Korean Restaurant, Jipbap Taste of Korea, Spoon House Korean Kitchen, and SGD Du Bu**. All of these restaurants are within a short distance from the CS building...
>
> ---
>
> **Turn 2 — User:** *Which of those is the highest rated?*
>
> **Assistant:** The highest rated Korean restaurant near the Siebel Center for Computer Science is **SGD Du Bu with a rating of 4.0 / 5.0**, followed by Jipbap Taste of Korea with a rating of 3.9 / 5.0. Other Korean restaurants in the area include Yogi Korean Restaurant (3.2 / 5.0) and Spoon House Korean Kitchen...
>
> ---
>
> **Turn 3 — User:** *What is the price level for that one?*
>
> **Assistant:** The price level for **SGD Du Bu is N/A**. In comparison, Jipbap Taste of Korea has a price level of $, and Spoon House Korean Kitchen has a price level of $$...

**Why this is real memory and not topic overlap:**
- *Turn 2 resolves "those"* — the LLM restricts its answer to the four Korean restaurants from Turn 1, even though the underlying retrieval pulls a slightly different chunk set when the query becomes `"What Korean restaurants are near... Which of those is the highest rated?"`. If memory were absent, Turn 2 would interpret "the highest rated" globally (returning, say, Huggermugger 5.0★) and ignore Korean entirely.
- *Turn 3 resolves "that one"* — "that one" has no semantic content. Without Turn 2 in context, the LLM cannot know that "that one" = SGD Du Bu. The response correctly threads SGD Du Bu through.

**How memory is enforced in the prompt:** the system prompt is unchanged, but the user turn for each follow-up appends an explicit instruction: *"If the question refers to a prior turn ('those', 'the second one', 'that place'), resolve the reference using the earlier messages in this conversation."* — see `query.py:ask_with_history`.

**Try it live:** launch `python app.py`, click the **Chat (conversational memory)** tab, and run the 3-turn sequence from the Examples panel.

---

## Stretch Feature — Chunking Strategy Comparison

**What was compared:** the production strategy (Strategy A: one chunk per document, ~640–790 chars each, 100 chunks total) against a textbook fixed-size strategy (Strategy B: 200-character sliding windows with 50-char overlap, **435 chunks total**) on the same three retrieval queries. `ingest.chunk_documents_fixed()` implements Strategy B and `demo_chunking_comparison.py` builds a second ChromaDB collection (`.chroma_fixed200`) and runs both side by side.

**Headline result: Strategy A is decisively better on this corpus.** The most striking case is Query 1 ("Korean restaurants") where Strategy B returns *zero* actual Korean restaurants in its top-5 — every result is a tail chunk that survived without the restaurant's category. Concrete evidence:

**Query 1 — "What Korean restaurants are near the CS building?"**

| Rank | Strategy A (whole-doc) | Strategy B (200-char windows) | What Strategy B's chunk actually contains |
|------|------------------------|-------------------------------|--------------------------------------------|
| 1 | Yogi Korean Restaurant ✅ | SGD Dubu (Korean — but lucky) | `' - Asian food - Takeout / delivery - Quick lunch near CS'` |
| 2 | Jipbap Taste of Korea ✅ | Golden Wheat (Chinese ❌) | `' == - Highly rated - Asian food - Quick lunch near CS'` |
| 3 | Spoon House Korean Kitchen ✅ | Susuru Ramen Bar (Japanese ❌) | `'- Asian food - Takeout / delivery - Late night ...'` |
| 4 | SGD Du Bu ✅ | Oozu Ramen Bar (Japanese ❌) | `'ighly rated - Asian food - Takeout / delivery ...'` |
| 5 | Nanjing Bistro (Chinese — adjacent) | Panda Express (Chinese ❌) | `'ood - Asian food - Takeout / delivery ...'` |

Strategy B fragments every document so that the **trailing `== USEFUL FOR ==` block — which lists generic tags like "Asian food", "Late night", "Quick lunch near CS" — becomes its own chunk, severed from the `Restaurant:` and `Categories:` lines**. The embedding for that tail chunk is identical-ish across many Asian restaurants. Result: the retriever picks based on tags alone and the restaurant identity is gone.

**Query 2 — "Where can I get ramen near the CS department?"**

| Rank | Strategy A | Strategy B |
|------|------------|------------|
| 1 | Susuru Ramen Bar | Oozu Ramen Bar |
| 2 | Oozu Ramen Bar | Susuru Ramen Bar (chunk 0) |
| 3 | Noodles and Company | Kajiken |
| 4 | Kajiken | **Susuru Ramen Bar (chunk 300)** ← duplicate |
| 5 | Spicy Tang | **Susuru Ramen Bar (chunk 150)** ← duplicate |

Strategy A finds 4 unique relevant restaurants. Strategy B's top-5 contains **Susuru Ramen Bar three times**, because three different windows of the same document all match the query separately. The user effectively gets only 3 unique restaurants instead of 5. This is the classic duplicate-results failure mode of fixed-size chunking over short documents.

**Query 3 — "Which coffee shops within 0.5 miles of Siebel have a rating above 4.0?"**

| Rank | Strategy A | Strategy B |
|------|------------|------------|
| 1 | BrewLab Coffee (4.4★) | **Etc Coffeehouse (0.0★)** |
| 2 | Starbucks (0.0★) | BrewLab Coffee (4.4★) |
| 3 | STARBUCKS (2.0★) | Cotti Coffee (4.5★) |
| 4 | Dutch Bros Coffee (4.3★) | Caffe Bene (4.1★) |
| 5 | Cotti Coffee (4.5★) | Cracked on Green (4.0★) |

This is the one query where Strategy B does *something* useful: by isolating the `Categories: Coffee & Tea Rating: X` line into a single small chunk, it surfaces Caffe Bene and Cracked on Green which Strategy A's broader chunks miss. But it still puts Etc Coffeehouse (0.0★) at rank 1 — the same kind of rating-blindness Strategy A has. Net: Strategy B has marginally better category recall on this single query but at the cost of catastrophic failure on Query 1.

**Why Strategy A wins for this corpus:** these are *structured records*, not narrative text. Each document is a tight 460–830 character profile where the restaurant's name, distance, category, rating, and price must be co-located to answer any practical query. Fixed-size chunking severs those relationships because the document is barely larger than 3 windows — there is no long-range context to preserve and overlap creates duplicates instead. Whole-document chunking would fail on a 50-page PDF, but for 100 short profiles it is exactly the right tradeoff.

**Quantitative summary** (correct top-5 relevant restaurants per query):

| Query | Strategy A relevant in top-5 | Strategy B relevant in top-5 |
|-------|------------------------------|------------------------------|
| Q1 Korean | 4 of 4 in corpus | 1 of 4 (SGD Dubu — and arguably by luck) |
| Q2 Ramen | 3 of 3 in corpus | 3 of 3 — but only 3 unique (2 duplicates) |
| Q3 Coffee ≥4.0 | 3 of 8 | 4 of 8 |

**Run it:** `python demo_chunking_comparison.py` rebuilds the alt collection and reproduces these tables live.

---

## Stretch Feature — Hybrid Search (BM25 + Dense)

**What was added:** `hybrid.py` builds a BM25 index over the same 100 chunks and fuses its ranking with the existing dense (`all-MiniLM-L6-v2` + ChromaDB cosine) ranking using **Reciprocal Rank Fusion (RRF)**:

> RRF_score(d) = (w_dense / (k + rank_dense(d))) + (w_bm25 / (k + rank_bm25(d)))

with `k = 60` (Cormack et al., 2009). Documents not in a method's top-N contribute 0 from that method. RRF combines *ranks*, not raw scores, which avoids the score-normalization problem — dense cosine similarities and BM25 scores live on incompatible scales. Weights default to 1.0/1.0 (balanced) but `hybrid_search(query, weight_dense=..., weight_bm25=...)` lets either method dominate.

**Why hybrid:** dense embeddings catch paraphrases ("ramen" ≈ "noodles") but underweight exact-token signal. BM25 catches rare-word and exact-name matches ("halal", "Huggermugger") but misses paraphrases. Combining them lets each method correct the other's weakness.

**Comparison on 3 queries (top-5 from each method, full output in `demo_hybrid_search.py`):**

**Query A — "Where can I get ramen near the CS department?"** (a paraphrase query — dense should help)

| Rank | Dense (cosine) | BM25 | Hybrid (RRF) |
|------|----------------|------|--------------|
| 1 | Susuru Ramen Bar (0.638) | Come Get This (8.32) | **Susuru Ramen Bar** |
| 2 | Oozu Ramen Bar (0.604) | Susuru Ramen Bar (7.36) | **Oozu Ramen Bar** |
| 3 | Noodles and Company (0.453) | Oozu Ramen Bar (7.33) | **Kajiken** |
| 4 | Kajiken (0.452) | Kajiken (4.65) | Smoothie King |
| 5 | Spicy Tang (0.439) | Huggermugger (1.73) | Come Get This |

*Which won:* **Hybrid.** Dense top-5 contains the three true ramen shops plus Noodles and Company (semantically adjacent) and Spicy Tang (a stretch). BM25's #1 is "Come Get This" — a Chinese take-out place — because its document text happens to contain the keyword "near" with high inverse-document-frequency weight. Hybrid promotes all three ramen shops to the top 3 and demotes both methods' noise.

**Query B — "Huggermugger restaurant"** (a rare exact name — BM25 should help)

| Rank | Dense (cosine) | BM25 | Hybrid (RRF) |
|------|----------------|------|--------------|
| 1 | **Huggermugger** (0.707) | **Huggermugger** (8.52) | **Huggermugger** |
| 2 | MrBeast Burger (0.516) | Yogi Korean Restaurant (1.32) | MrBeast Burger |
| 3 | Royal BBQ (0.483) | Perkins American Food (1.02) | Perkins American Food |
| 4 | Burger King (0.481) | interlude (0.86) | Beckman Cafe |
| 5 | Beckman Cafe (0.469) | J6 Kitchen (0.85) | J6 Kimbap |

*Which won:* **Both Dense and BM25 nailed #1; Hybrid kept it.** Dense did fine on this query because "Huggermugger" is so unique that even on character-level subword overlap it dominates. The interesting observation is BM25's massive score gap (8.52 vs 1.32) — far larger than dense's (0.707 vs 0.516) — which is exactly BM25's strength: when the rare token is present in only one document, the score gap is decisive.

**Query C — "halal late night quick lunch"** (multi-word descriptive — hybrid should help)

| Rank | Dense (cosine) | BM25 | Hybrid (RRF) |
|------|----------------|------|--------------|
| 1 | Atomic Wings (0.524) | Atomic Wings (6.01) | **Atomic Wings** |
| 2 | Mid-Summer Lounge (0.489) | **Garbanzo Mediterranean Fresh** (4.93) | **Garbanzo Mediterranean Fresh** |
| 3 | McDonald's (0.489) | Legends (2.50) | Burger King |
| 4 | Einstein Bros. Bagels (0.482) | Shanghai 1938 (2.50) | Kajiken |
| 5 | Kajiken (0.476) | Subway (2.50) | Pho Noodle Station |

*Which won:* **Hybrid.** Atomic Wings carries the literal `Halal` category tag and both methods rank it #1. The interesting case is **Garbanzo Mediterranean Fresh**, which also has `Halal` in its `== USEFUL FOR ==` block but does *not* appear in dense's top-5 (dense scores it lower because "Mediterranean" pulls its embedding away from the "late night / quick lunch" descriptors). BM25 catches it via direct token match on "halal." Hybrid promotes it to rank 2 — the user gets both halal options instead of just one.

**Summary:** the three queries demonstrate the three regimes:
- **Paraphrase-heavy** (Query A) — hybrid stabilizes a noisy BM25 tail with dense's semantic signal.
- **Exact-token / rare name** (Query B) — both methods agree; hybrid loses nothing.
- **Multi-feature** (Query C) — hybrid recovers a relevant document that dense alone would miss.

**Run it:** `python demo_hybrid_search.py` reproduces these tables live.

---

## Stretch Feature — Metadata Filtering

**What was added:** `ingest.parse_metadata()` extracts four structured numeric fields from each document — `rating`, `review_count`, `distance_miles`, and `price_level` (0–4, where N/A=0, $=1, $$=2, $$$=3, $$$$=4) — and `embed.build_vectorstore()` stores them as ChromaDB metadata alongside the embedded text. Two new APIs use them:

- `embed.retrieve(query, k=5, where=...)` — semantic search **with** a metadata filter applied at retrieval time, so the vector index never returns chunks that violate the constraint.
- `embed.metadata_query(where=..., order_by=...)` — **pure** metadata query with no vector similarity, for "most reviews / cheapest / closest / highest rated" questions where semantic embeddings cannot rank numerically.

**Why this matters:** the *Failure Case Analysis* below identifies semantic search's inability to filter or sort on numeric fields as the root cause of three of the five evaluation failures. Metadata filtering directly fixes that.

**Before vs. after — same 4 evaluation queries:**

| Q | Question | Before (pure semantic, top-5) | After (with metadata filter / sort) | Accuracy |
|---|----------|-------------------------------|-------------------------------------|----------|
| 1 | Closest restaurant to Siebel? | Circle K (0.28 mi) — wrong, Espresso Royale never retrieved | **Espresso Royale – Grainger (0.09 mi)** — `metadata_query(order_by='distance_miles', descending=False)` | ❌ → ✅ |
| 3 | Coffee shops rated ≥ 4.0? | BrewLab (4.4★), Starbucks (0.0★), STARBUCKS (2.0★), Dutch Bros (4.3★), Cotti (4.5★) — 2 of 5 violate filter | **BrewLab (4.4★), Espresso Royale (4.0★), Cotti (4.5★), Caffe Bene (4.1★), Dutch Bros (4.3★)** — `retrieve("coffee shops near Siebel", where={"rating": {"$gte": 4.0}})` | ⚠️ → ✅ |
| 4 | Cheap ($) restaurants rated > 4.0? | Circle K, Far East, Murphy's Pub, Sbarro, Evo Cafe — *none* match both criteria; system said "I don't have enough information" | **Huggermugger (5.0★), Paris Super Crepes (4.2★), Signature Grill (4.2★), Cravings (4.1★), Latea (4.1★)** — `metadata_query(where={"$and": [{"price_level": {"$eq": 1}}, {"rating": {"$gt": 4.0}}]})` | ❌ → ✅ |
| 5 | Restaurant with the most Yelp reviews? | Legends (114 reviews) — wrong; Cravings never retrieved | **Cravings (217 reviews)** — `metadata_query(order_by='review_count', limit=1)` | ❌ → ✅ |

**Visible effect:** Q3 is the clearest demonstration of *filtering at retrieval time*. The pure-semantic top-5 contains two zero-rated Starbucks entries because "Starbucks" is highly similar to "coffee shop" in embedding space. Adding `where={"rating": {"$gte": 4.0}}` to the same query removes them and the next-highest-similarity legitimate matches (Cotti, Caffe Bene, Dutch Bros) take their place — same query, same embedding, different (correct) result set.

**Updated evaluation score:** the original evaluation report (below) reflects pure-semantic retrieval. With the metadata filter, **4 of the 5 evaluation questions now answer correctly** (Q2 was already correct), and Q5's failure case identified in *Failure Case Analysis* is no longer a failure.

---

## Query Interface

**Interface:** Gradio web app (`app.py`), launched with `python app.py`, accessible at `http://localhost:7860`.

**Input field:** Single text box labeled "Your question" — accepts any natural-language question about restaurants near Siebel Center.

**Output fields:**
- *Answer* (large text box) — grounded response from `llama-3.3-70b-versatile`, citing restaurant names inline.
- *Documents retrieved* (smaller text box) — bulleted list of the 5 source document names used to generate the answer.

**Sample interaction transcript:**

```
User: What Korean restaurants are near the CS building?

Answer:
The Korean restaurants near the Siebel Center for Computer Science (CS building) are
Yogi Korean Restaurant, Jipbap Taste of Korea, Spoon House Korean Kitchen, and SGD Du Bu.
All of these restaurants are within a short distance from the CS building, with Yogi Korean
Restaurant and Jipbap Taste of Korea being 0.35 miles away, Spoon House Korean Kitchen
being 0.33 miles away, and SGD Du Bu being 0.42 miles away.

Documents retrieved:
• Yogi Korean Restaurant
• Jipbap Taste Of Korea
• Spoon House Korean Kitchen
• Sgd Du Bu
• Nanjing Bistro
```

---

## Spec Reflection

**One way the spec helped you during implementation:** Writing the Evaluation Plan in planning.md before coding forced me to commit to five specific, verifiable questions with expected answers. When I ran the system and Q5 ("most Yelp reviews") returned the wrong restaurant, I had a clear ground truth to compare against — I knew immediately that Cravings (217 reviews) was the correct answer and that Legends (114) was wrong. Without the pre-written expected answers, I might have accepted the LLM's response as plausible. The spec turned a vague sense that "something seemed off" into a precisely identified retrieval failure.

**One way your implementation diverged from the spec, and why:** The planning.md spec listed review snippets (user review text) as a key data field in each document, but all 100 documents ended up without any review text. The Yelp Fusion API's free tier removed access to the `/reviews` endpoint, and direct web scraping was blocked by Cloudflare bot detection. I updated the chunking strategy accordingly — whole-document chunks still work because the metadata fields (rating, categories, price, distance, hours) carry enough semantic signal for most query types. The one class of queries that genuinely suffers from the missing review text is opinion-based questions ("which place has the best atmosphere?"), which the system correctly declines to answer.

---

## AI Usage

**Instance 1 — Data collection script**

- *What I gave the AI:* The domain description (restaurants within 0.5 miles of Siebel Center), the Yelp Fusion API documentation, and the list of fields to collect (name, address, distance, categories, rating, review count, price, phone, hours, Yelp URL).
- *What it produced:* A Python script (`scrape_yelp.py`) using `requests` and `python-dotenv` that called the Yelp search endpoint by coordinates and radius, fetched business details per restaurant, computed haversine distance, and wrote structured `.txt` files to `documents/`.
- *What I changed or overrode:* The initial script used `convert_to_list=True` in the encoding call, which failed with the installed sentence-transformers version. I diagnosed the API mismatch and corrected it to `.tolist()`. I also changed the radius from 1600m to 800m (0.5 miles) after the first run returned restaurants I considered too far from Siebel Center, and I removed the review-fetching code entirely after confirming the API endpoint returned 404 for all restaurants on the free tier.

**Instance 2 — Embedding and retrieval pipeline**

- *What I gave the AI:* The Retrieval Approach section from planning.md (model name, top-k value, ChromaDB as vector store) and the pipeline architecture diagram showing the five stages.
- *What it produced:* `embed.py` with `build_vectorstore()` and `retrieve()` functions using `sentence-transformers` and `chromadb.PersistentClient`, storing source filenames as metadata and querying with cosine similarity.
- *What I changed or overrode:* The generated code passed `convert_to_list=True` to `model.encode()`, which the installed version rejected. I fixed this to `.tolist()` after reading the traceback. I also added a `client.delete_collection()` call before `create_collection()` so re-running the script rebuilds the index cleanly rather than erroring on a duplicate collection name — the AI-generated version assumed the collection never existed.

**Instance 3 — Inline citations in the Gradio UI**

- *What I gave the AI:* The existing `app.py` (which only printed retrieved source filenames as a plain bulleted list) and the requirement to surface citations *inline* in the answer text, with each citation linking to the corresponding Yelp page. I also pointed to the `Source URL:` field in each document's header as the source of truth for URLs.
- *What it produced:* `extract_citation()` in `query.py` that pulls `Restaurant:` and `Source URL:` out of each retrieved chunk via regex, plus `inject_inline_citations()` in `app.py` that finds the first mention of each restaurant name in the LLM's answer and rewrites it as `Name [[N]](url)` so the marker renders as a clickable footnote in Markdown. The output components were also changed from `gr.Textbox` to `gr.Markdown` to render the links.
- *What I changed or overrode:* The first version of `inject_inline_citations()` used a plain `str.replace()` and processed sources in their original retrieval order, which caused a bug where a shorter name (e.g. "Spoon House") could match inside a longer one (e.g. "Spoon House Korean Kitchen") before the longer name was processed. I added `\b...\b` word boundaries and changed the loop to sort sources by descending name length so the longest matches always win. I also kept the numbered footnote list at the bottom even for sources not mentioned inline, so the user can always see all five retrieved documents — the AI-generated version had dropped them.
