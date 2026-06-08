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

**Chunk size:** ~700 characters (whole document). Each restaurant `.txt` file is 461–834 characters; the entire file becomes one chunk.

**Overlap:** 0. Each restaurant document is fully independent — there is no information that spans two files, so overlap would add noise without benefit.

**Why these choices fit your documents:** These are structured records, not narrative text. A query about "cheap Korean food near CS" needs the restaurant's price, category, and distance to be in the same chunk. Splitting by fixed character count would break exactly those relationships (e.g., cutting between the METADATA section and the USEFUL FOR tags). Whole-document chunks keep every field co-located so the embedding encodes the full restaurant profile as a single semantic unit. Documents were already clean plain text from the Yelp API — no HTML stripping was needed beyond normalizing whitespace.

**Final chunk count:** 100 (one per restaurant).

**Sample chunks:**

| # | Source document | Chunk excerpt |
|---|----------------|---------------|
| 1 | `restaurant_espresso_royale_grainger_engineering_library.txt` | `Restaurant: Espresso Royale – Grainger Engineering Library / Distance from Siebel Center: 0.09 miles / Categories: Coffee Roasteries, Coffee & Tea / Rating: 4.0 / 5.0 / Price Level: N/A` |
| 2 | `restaurant_oozu_ramen_bar.txt` | `Restaurant: Oozu Ramen Bar / Distance: 0.34 miles / Categories: Ramen / Rating: 4.0 / 5.0 / Price Level: $$ / Opening Hours: Mon: 11:30-22:00 ... / USEFUL FOR: Cheap food, Asian food, Late night` |
| 3 | `restaurant_jipbap_taste_of_korea.txt` | `Restaurant: Jipbap Taste of Korea / Distance: 0.35 miles / Categories: Korean / Rating: 3.9 / 5.0 / Price Level: $ / USEFUL FOR: Cheap food, Asian food, Takeout / delivery` |
| 4 | `restaurant_brewlab_coffee.txt` | `Restaurant: BrewLab Coffee / Distance: 0.43 miles / Categories: Coffee & Tea / Rating: 4.4 / 5.0 / Price Level: $$ / USEFUL FOR: Highly rated, Coffee / cafe, Takeout / delivery` |
| 5 | `restaurant_cracked_on_green.txt` | `Restaurant: Cracked on Green / Distance: 0.36 miles / Categories: Coffee & Tea, Breakfast & Brunch, Food Trucks / Rating: 4.0 / 5.0 / Price Level: $ / USEFUL FOR: Cheap food, Highly rated, Breakfast / brunch, Late night` |

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
