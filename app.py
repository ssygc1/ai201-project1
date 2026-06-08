"""
Milestone 5 — Gradio query interface.

Run with: python app.py
Then open http://localhost:7860
"""

import gradio as gr
from query import ask


def handle_query(question: str):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    source_lines = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], source_lines


with gr.Blocks(title="UIUC CS Nearby Restaurant Guide") as demo:
    gr.Markdown(
        """
        # UIUC CS Nearby Restaurant Guide
        Ask about restaurants within 0.5 miles of **Siebel Center for Computer Science**.
        Answers are grounded in Yelp data collected June 2026.
        """
    )

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
            answer = gr.Textbox(label="Answer", lines=8, interactive=False)
        with gr.Column(scale=1):
            sources = gr.Textbox(label="Documents retrieved", lines=8, interactive=False)

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


if __name__ == "__main__":
    demo.launch()
