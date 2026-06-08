"""
Milestone 5 — Gradio query interface (single-query + multi-turn chat).

Run with: python app.py
Then open http://localhost:7860
"""

import re
import gradio as gr
from query import ask, ask_with_history


def inject_inline_citations(answer: str, sources: list[dict]) -> str:
    """
    Replace the first mention of each retrieved restaurant name in `answer`
    with `Name [[N]](url)` so citations render inline as clickable markers.
    Longest names are matched first so e.g. "Spoon House Korean Kitchen" is
    linked before a shorter substring of it.
    """
    indexed = list(enumerate(sources, 1))
    indexed.sort(key=lambda x: len(x[1]["name"]), reverse=True)

    for n, s in indexed:
        name, url = s["name"], s["url"]
        if not name or not url:
            continue
        pattern = re.compile(r"\b" + re.escape(name) + r"\b")
        replacement = f"{name} [[{n}]]({url})"
        answer, _ = pattern.subn(replacement, answer, count=1)
    return answer


def handle_query(question: str):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)
    sources = result["sources"]
    answer_md = inject_inline_citations(result["answer"], sources)
    footnotes = "\n".join(
        f"{i}. [{s['name']}]({s['url']})" if s["url"] else f"{i}. {s['name']}"
        for i, s in enumerate(sources, 1)
    )
    return answer_md, footnotes


def handle_chat(message: str, history: list[dict]) -> tuple[str, list[dict]]:
    """
    Multi-turn chat handler. `history` follows Gradio 6's messages format
    (list of {"role": "user"|"assistant", "content": str}). We convert it
    to the (user, assistant) tuple list that ask_with_history expects.
    """
    if not message.strip():
        return "", history

    pairs: list[tuple[str, str]] = []
    pending_user = None
    for turn in history:
        if turn["role"] == "user":
            pending_user = turn["content"]
        elif turn["role"] == "assistant" and pending_user is not None:
            pairs.append((pending_user, turn["content"]))
            pending_user = None

    result = ask_with_history(message, pairs)
    answer_md = inject_inline_citations(result["answer"], result["sources"])

    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": answer_md},
    ]
    return "", history


with gr.Blocks(title="UIUC CS Nearby Restaurant Guide") as demo:
    gr.Markdown(
        """
        # UIUC CS Nearby Restaurant Guide
        Ask about restaurants within 0.5 miles of **Siebel Center for Computer Science**.
        Answers are grounded in Yelp data collected June 2026.
        """
    )

    with gr.Tabs():
        with gr.Tab("Single query"):
            with gr.Row():
                with gr.Column():
                    question = gr.Textbox(
                        label="Your question",
                        placeholder="e.g. Which coffee shops near the CS building are rated above 4 stars?",
                        lines=2,
                    )
                    ask_btn = gr.Button("Ask", variant="primary")

            with gr.Row():
                with gr.Column(scale=2):
                    answer = gr.Markdown(label="Answer")
                with gr.Column(scale=1):
                    sources = gr.Markdown(label="Documents retrieved")

            ask_btn.click(fn=handle_query, inputs=question, outputs=[answer, sources])
            question.submit(fn=handle_query, inputs=question, outputs=[answer, sources])

            gr.Examples(
                examples=[
                    "What Korean restaurants are near the CS building?",
                    "Which coffee shops within 0.5 miles of Siebel have a rating above 4.0?",
                    "Which cheap restaurants near Siebel have a good Yelp rating?",
                    "Where can I get ramen near the CS department?",
                    "Which restaurant near Siebel has the most Yelp reviews?",
                    "Which professor teaches CS 447 at UIUC?",
                ],
                inputs=question,
            )

        with gr.Tab("Chat (conversational memory)"):
            gr.Markdown(
                "Follow-up questions can reference earlier turns "
                "(e.g. *'which of those is the cheapest?'*) — prior messages "
                "are included in the prompt so the LLM can resolve the reference."
            )
            chatbot = gr.Chatbot(height=400)
            with gr.Row():
                chat_input = gr.Textbox(
                    placeholder="Ask a follow-up...",
                    scale=4,
                    show_label=False,
                )
                send_btn = gr.Button("Send", variant="primary", scale=1)
                clear_btn = gr.Button("Clear", scale=1)

            send_btn.click(handle_chat, [chat_input, chatbot], [chat_input, chatbot])
            chat_input.submit(handle_chat, [chat_input, chatbot], [chat_input, chatbot])
            clear_btn.click(lambda: [], None, chatbot)

            gr.Examples(
                examples=[
                    ["What Korean restaurants are near the CS building?"],
                    ["Which of those is the highest rated?"],
                    ["And which has the most Yelp reviews?"],
                ],
                inputs=chat_input,
                label="Try this 3-turn sequence",
            )


if __name__ == "__main__":
    demo.launch()
