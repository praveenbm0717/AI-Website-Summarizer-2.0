import os
import gradio as gr
from summarizer import summarize

# --------------------------
# Custom CSS
# --------------------------

CSS = """
body{
    background:#0f172a;
}

.gradio-container{
    max-width:1250px !important;
    margin:auto;
}

footer{
    visibility:hidden;
}

.title{
    text-align:center;
    padding:15px;
}

.title h1{
    font-size:42px;
    color:#60a5fa;
    margin-bottom:5px;
}

.title p{
    color:#cbd5e1;
    font-size:18px;
}

.stats{
    text-align:center;
    padding:18px;
    border-radius:15px;

    background:#ffffff;

    color:#111827;

    border:2px solid #3b82f6;

    box-shadow:0 8px 18px rgba(0,0,0,.12);

    font-size:18px;

    font-weight:bold;
}

.gr-button-primary{
    background:#2563eb !important;
    border:none !important;
    border-radius:10px !important;
    font-size:18px !important;
}

.gr-button-primary:hover{
    background:#1d4ed8 !important;
}
"""

# --------------------------
# UI
# --------------------------

with gr.Blocks(
    title="AI Website Summarizer",
    css=CSS,
    theme=gr.themes.Soft()
) as demo:

    gr.HTML("""
    <div class="title">
        <h1>🤖 AI Website Summarizer</h1>
        <p>Summarize any website instantly using Groq + Llama 3.3</p>
    </div>
    """)

    with gr.Row():

        # --------------------------
        # Left Panel
        # --------------------------

        with gr.Column(scale=1):

            url = gr.Textbox(
                label="🌐 Website URL",
                placeholder="https://example.com",
                lines=1
            )

            summarize_btn = gr.Button(
                "🚀 Generate Summary",
                variant="primary"
            )

            clear_btn = gr.ClearButton(
                components=[url]
            )

            gr.Examples(
                examples=[
                    ["https://openai.com"],
                    ["https://github.com"],
                    ["https://python.org"],
                    ["https://www.flipkart.com"],
                    ["https://en.wikipedia.org/wiki/Artificial_intelligence"]
                ],
                inputs=url
            )

        # --------------------------
        # Right Panel
        # --------------------------

        with gr.Column(scale=2):

            summary = gr.Markdown(
                value="""
# 👋 Welcome

Enter a website URL and click **Generate Summary**.
"""
            )

            with gr.Row():

                words = gr.Markdown(
                    value="### 📝 Words\n0",
                    elem_classes="stats"
                )

                chars = gr.Markdown(
                    value="### 📄 Characters\n0",
                    elem_classes="stats"
                )

                time_taken = gr.Markdown(
                    value="### ⏱ Time\n0 sec",
                    elem_classes="stats"
                )

    summarize_btn.click(
        fn=summarize,
        inputs=url,
        outputs=[
            summary,
            words,
            chars,
            time_taken
        ]
    )

    gr.Markdown("""
---

## ⚡ Tech Stack

- 🐍 Python
- 🕷 BeautifulSoup
- 🚀 Groq API
- 🧠 Llama 3.3 70B
- 🎨 Gradio

Made with ❤️ by **Praveen B M**
""")

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )