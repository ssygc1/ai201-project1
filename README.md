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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
