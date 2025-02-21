import gradio as gr
import base64
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    base_url="http://localhost:6000",  # Thay bằng URL chính xác
    api_key="fake-key",  # Thay bằng API key thực tế
)

def process_inputs(image1, image2, image3, video, text):
    # Mã hóa các ảnh dưới dạng base64 nếu có
    images = [image1, image2, image3]
    image_data = []
    for img in images:
        if img is not None:
            with open(img, 'rb') as file:
                encoded_img = base64.b64encode(file.read()).decode('utf-8')
                image_data.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_img}"
                    },
                    "text" : text
                    #"description": f"Image: {os.path.basename(img)}"
                })
        
    message_content = [{"type": "text", "text": text}] + image_data 

    # Mã hóa video dưới dạng base64 nếu có
    if video:
        message_content.append({"type": "text", "text": f"Video URL: {video}"}) 

    # Gửi yêu cầu đến OpenAI
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": message_content}],
            max_tokens=300,
            model="VILA1.5-3B",
            extra_body={"num_beams": 1, "use_cache": False},
        )
        generated_text = response.choices[0].message.content[0]['text'] if response.choices else "No response generated."
    except Exception as e:
        generated_text = f"Error: {str(e)}"
    
    return generated_text

# Custom CSS
custom_css = """
.upload-box {
    border: 2px dashed #ccc;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    margin: 10px;
}
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}
"""

with gr.Blocks(css=custom_css) as demo:
    gr.HTML("<h1>VILA: On Pre-training for Visual Language Models</h1>")
    # Links row
    with gr.Row():
        gr.HTML('<a href="#">[Paper]</a>')
        gr.HTML('<a href="#">[Github]</a>')
    # Powered by row
    gr.HTML('Powered by TinyChat with 4-bit AWQ')
    # Input containers
    with gr.Row():
        # Three individual image inputs
        image1 = gr.Image(label="Image 1", elem_classes="upload-box", type="filepath")
        image2 = gr.Image(label="Image 2", elem_classes="upload-box", type="filepath")
        image3 = gr.Image(label="Image 3", elem_classes="upload-box", type="filepath")
        # Video input
        video = gr.Video(label="Video (12 frames max)", elem_classes="upload-box")
    # Text input and buttons
    with gr.Row():
        text_input = gr.Textbox(
            placeholder="Enter text and press ENTER",
            label="",
            lines=3
        )
    with gr.Row():
        submit_btn = gr.Button("Send", variant="primary")
        clear_btn = gr.Button("Clear")
    # Warning message
    gr.HTML("*** Before changing the current images, uploading new images or switching the prompt style, please click the clear button.")
    # Output area
    output = gr.Textbox(label="Assistant Response")
    # Set up event handlers
    submit_btn.click(
        fn=process_inputs,
        inputs=[image1, image2, image3, video, text_input],
        outputs=output
    )
    clear_btn.click(
        lambda: [None, None, None, None, ""],   
        outputs=[image1, image2, image3, video, text_input]
    )
    # Launch the interface
if __name__ == "__main__":
    demo.launch()
