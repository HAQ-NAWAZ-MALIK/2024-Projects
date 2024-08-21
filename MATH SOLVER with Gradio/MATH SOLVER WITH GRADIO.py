import gradio as gr
import os

os.system('pip install dashscope -U')
import tempfile
from pathlib import Path
import secrets
import dashscope
from dashscope import MultiModalConversation, Generation

API_KEY = os.getenv('API_KEY')
dashscope.api_key = API_KEY
conversation_history = []

def handle_image_upload(image):
    global conversation_history
    conversation_history = []  # Reset history with each new image upload
    
    temp_dir = os.environ.get("GRADIO_TEMP_DIR") or str(Path(tempfile.gettempdir()) / "gradio")
    os.makedirs(temp_dir, exist_ok=True)
    
    temp_filename = f"image_{secrets.token_hex(16)}.jpg"
    image_path = os.path.join(temp_dir, temp_filename)
    image.save(image_path)

    # Set up messages for OCR processing
    messages = [{
        'role': 'system',
        'content': [{'text': 'You are an efficient assistant.'}]
    }, {
        'role': 'user',
        'content': [
            {'image': f'file://{image_path}'},
            {'text': 'Please extract and describe any math-related content from this image, including LaTeX formatting for formulas.'}
        ]
    }]
    
    response = MultiModalConversation.call(model='qwen-vl-max-0809', messages=messages)
    
    os.remove(image_path)  # Clean up temporary image file
    
    return response.output.choices[0]["message"]["content"]

def generate_math_solution(image_desc, query):
    global conversation_history
    if not conversation_history:
        conversation_history.append({'role': 'system', 'content': 'You are a diligent math assistant.'})
    conversation_history = conversation_history[:1] + conversation_history[1:][-4:]

    if image_desc:
        content = f'Image description: {image_desc}\n\n'
    else:
        content = ''
    user_query = f"{content}User query: {query}"
    conversation_history.append({'role': 'user', 'content': user_query})

    response = Generation.call(
        model="qwen2-math-72b-instruct",
        messages=conversation_history,
        result_format='message',
        stream=True
    )
    
    final_answer = None
    for resp in response:
        if resp.output is None:
            continue
        final_answer = resp.output.choices[0].message.content
        yield final_answer.replace("\\", "\\\\")
    
    print(f'Query: {user_query}\nAnswer: {final_answer}')
    if final_answer is None:
        conversation_history.pop()
    else:
        conversation_history.append({'role': 'assistant', 'content': final_answer})

def math_assistant(image, question):
    image_desc = handle_image_upload(image) if image else None
    yield from generate_math_solution(image_desc, question)

custom_css = """
#math-app .katex-display { display: inline; }
#math-app .katex-display>.katex { display: inline; }
#math-app .katex-display>.katex>.katex-html { display: inline; }
"""

# Define the interface
interface = gr.Interface(
    css=custom_css,
    fn=math_assistant,
    inputs=[
        gr.Image(type="pil", label="Upload Image"),
        gr.Textbox(label="Enter Your Question")
    ],
    outputs=gr.Markdown(label="Solution", latex_delimiters=[
        {"left": "\\(", "right": "\\)", "display": True},
        {"left": "\\begin{equation}", "right": "\\end{equation}", "display": True},
        {"left": "\\begin{align}", "right": "\\end{align}", "display": True},
        {"left": "\\begin{alignat}", "right": "\\end{alignat}", "display": True},
        {"left": "\\begin{gather}", "right": "\\end{gather}", "display": True},
        {"left": "\\begin{CD}", "right": "\\end{CD}", "display": True},
        {"left": "\\[", "right": "\\]", "display": True}
    ], elem_id="math-app"),
    # title="🔢 Math Solver Interface",
    allow_flagging='never',
    description="""\
<p align="center"><img src="https://modelscope.oss-cn-beijing.aliyuncs.com/resource/qwen.png" style="height: 60px"/><p>"""
    """<center><font size=8>🔢 Math Solver Interface</center>"""
    """\
<center><font size=3>This application leverages Qwen2-VL for OCR and Qwen2-Math for solving mathematical problems. You can input images or text to get precise mathematical solutions.</center>"""
)    

# Launch the Gradio app
interface.launch()
