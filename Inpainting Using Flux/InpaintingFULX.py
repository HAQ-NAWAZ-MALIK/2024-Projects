from typing import Tuple

import requests
import random
import numpy as np
import gradio as gr
import spaces
import torch
from PIL import Image
from diffusers import FluxInpaintPipeline

INTRO_TEXT = """
# FLUX.1 Inpainting 🔥
Special thanks to [Black Forest Labs](https://huggingface.co/black-forest-labs) for 
developing this fantastic model, and big appreciation to [Gothos](https://github.com/Gothos) 
for enhancing it to support inpainting with FLUX.
"""

MAX_SEED_VALUE = np.iinfo(np.int32).max
DEFAULT_IMAGE_SIZE = 1024
DEVICE_TYPE = "cuda" if torch.cuda.is_available() else "cpu"

def remove_bg(image: Image.Image, threshold: int = 50) -> Image.Image:
    image = image.convert("RGBA")
    data = image.getdata()
    new_data = []
    for item in data:
        avg = sum(item[:3]) / 3
        if avg < threshold:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)

    image.putdata(new_data)
    return image

SAMPLE_INPUTS = [
    [
        {
            "background": Image.open(requests.get("https://media.roboflow.com/spaces/doge-2-image.png", stream=True).raw),
            "layers": [remove_bg(Image.open(requests.get("https://media.roboflow.com/spaces/doge-2-mask-2.png", stream=True).raw))],
            "composite": Image.open(requests.get("https://media.roboflow.com/spaces/doge-2-composite-2.png", stream=True).raw),
        },
        "little lion",
        42,
        False,
        0.85,
        30
    ],
    [
        {
            "background": Image.open(requests.get("https://media.roboflow.com/spaces/doge-2-image.png", stream=True).raw),
            "layers": [remove_bg(Image.open(requests.get("https://media.roboflow.com/spaces/doge-2-mask-3.png", stream=True).raw))],
            "composite": Image.open(requests.get("https://media.roboflow.com/spaces/doge-2-composite-3.png", stream=True).raw),
        },
        "tribal tattoos",
        42,
        False,
        0.85,
        30
    ]
]

pipeline = FluxInpaintPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16).to(DEVICE_TYPE)

def adjust_image_size(
    original_size: Tuple[int, int],
    max_size: int = DEFAULT_IMAGE_SIZE
) -> Tuple[int, int]:
    width, height = original_size

    if width > height:
        scale_factor = max_size / width
    else:
        scale_factor = max_size / height

    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    new_width -= new_width % 32
    new_height -= new_height % 32

    return new_width, new_height

@spaces.GPU(duration=100)
def generate_image(
    image_data: dict,
    text_prompt: str,
    seed_value: int,
    randomize_seed: bool,
    transformation_strength: float,
    inference_steps: int,
    progress=gr.Progress(track_tqdm=True)
):
    if not text_prompt:
        gr.Info("Please provide a text prompt.")
        return None, None

    background_image = image_data['background']
    mask_layer = image_data['layers'][0]

    if not background_image:
        gr.Info("Please upload an image.")
        return None, None

    if not mask_layer:
        gr.Info("Please draw a mask on the image.")
        return None, None

    width, height = adjust_image_size(original_size=background_image.size)
    resized_background = background_image.resize((width, height), Image.LANCZOS)
    resized_mask = mask_layer.resize((width, height), Image.LANCZOS)

    if randomize_seed:
        seed_value = random.randint(0, MAX_SEED_VALUE)
    generator = torch.Generator().manual_seed(seed_value)
    output_image = pipeline(
        prompt=text_prompt,
        image=resized_background,
        mask_image=resized_mask,
        width=width,
        height=height,
        strength=transformation_strength,
        generator=generator,
        num_inference_steps=inference_steps
    ).images[0]
    print('INFERENCE COMPLETED')
    return output_image, resized_mask

with gr.Blocks() as demo_interface:
    gr.Markdown(INTRO_TEXT)
    with gr.Row():
        with gr.Column():
            image_editor_component = gr.ImageEditor(
                label='Image',
                type='pil',
                sources=["upload", "webcam"],
                image_mode='RGB',
                layers=False,
                brush=gr.Brush(colors=["#FFFFFF"], color_mode="fixed"))

            with gr.Row():
                text_input_component = gr.Text(
                    label="Prompt",
                    show_label=False,
                    max_lines=1,
                    placeholder="Enter your prompt",
                    container=False,
                )
                submit_button = gr.Button(
                    value='Submit', variant='primary', scale=0)

            with gr.Accordion("Advanced Settings", open=False):
                seed_slider = gr.Slider(
                    label="Seed",
                    minimum=0,
                    maximum=MAX_SEED_VALUE,
                    step=1,
                    value=42,
                )

                random_seed_checkbox = gr.Checkbox(
                    label="Randomize seed", value=True)

                with gr.Row():
                    strength_slider = gr.Slider(
                        label="Strength",
                        info="Specifies how much to alter the original `image`. "
                             "Range is from 0 to 1. Higher values add more noise to the `image`, "
                             "starting from the original image.",
                        minimum=0,
                        maximum=1,
                        step=0.01,
                        value=0.85,
                    )

                    inference_steps_slider = gr.Slider(
                        label="Number of inference steps",
                        info="Number of denoising steps. More steps usually result in a higher quality image.",
                        minimum=1,
                        maximum=50,
                        step=1,
                        value=20,
                    )
        with gr.Column():
            output_image = gr.Image(
                type='pil', image_mode='RGB', label='Generated image', format="png")
            with gr.Accordion("Debug", open=False):
                output_mask = gr.Image(
                    type='pil', image_mode='RGB', label='Input mask', format="png")
    with gr.Row():
        gr.Examples(
            fn=generate_image,
            examples=SAMPLE_INPUTS,
            inputs=[
                image_editor_component,
                text_input_component,
                seed_slider,
                random_seed_checkbox,
                strength_slider,
                inference_steps_slider
            ],
            outputs=[
                output_image,
                output_mask
            ],
            run_on_click=True,
            cache_examples=True
        )

    submit_button.click(
        fn=generate_image,
        inputs=[
            image_editor_component,
            text_input_component,
            seed_slider,
            random_seed_checkbox,
            strength_slider,
            inference_steps_slider
        ],
        outputs=[
            output_image,
            output_mask
        ]
    )

demo_interface.launch(debug=False, show_error=True)
