import gradio as gr
from main import process_images

with gr.Blocks() as demo:
    gr.Markdown("## 🏞️ **Adobe Stock Image Metadata Generator**")

    with gr.Row(equal_height=True):
        api_key = gr.Textbox(label="🔐 API Key", type="password", placeholder="Enter your API key")

    with gr.Row(equal_height=True):   
        with gr.Column(scale=1):     
            title_length = gr.Number(label="🔠 Max Title Length", value=70, minimum=10, maximum=150)
            max_keywords = gr.Number(label="🏷️ Max Keywords", value=45, minimum=5, maximum=50)
            use_filename = gr.Checkbox(label="📝 Use Filename for Analysis", value=False)
        folder_input = gr.File(label="📁 Select a Folder", file_count="directory")

    run_btn = gr.Button("▶️ Generate Metadata", variant="primary")

    output_gallery = gr.Gallery(label="🖼️ Generated Metadata Previews", columns=3, object_fit="contain", height="auto")
    metadata_csv = gr.File(label="📄 Download Metadata CSV")

    run_btn.click(
        fn=process_images,
        inputs=[folder_input, api_key, title_length, max_keywords, use_filename],
        outputs=[output_gallery, metadata_csv]
    )

if __name__ == "__main__":
    demo.launch()
