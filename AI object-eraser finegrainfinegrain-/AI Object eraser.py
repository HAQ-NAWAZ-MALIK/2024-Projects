import io
from typing import Any

import gradio as gr
import httpx
from environs import Env
from gradio_image_annotation import image_annotator
from gradio_imageslider import ImageSlider
from PIL import Image

env = Env()
env.read_env()

with env.prefixed("ERASER_"):
    API_URL: str = str(env.str("API_URL", "https://spaces.finegrain.ai/eraser"))
    API_KEY: str | None = env.str("API_KEY", None)
    CA_BUNDLE: str | None = env.str("CA_BUNDLE", None)

auth = None if API_KEY is None else httpx.BasicAuth("hf", API_KEY)


def process_bbox(
    prompts: dict[str, Any],
    request: gr.Request | None,
) -> tuple[Image.Image, Image.Image]:
    assert isinstance(img := prompts["image"], Image.Image)
    assert isinstance(boxes := prompts["boxes"], list)
    assert len(boxes) == 1
    assert isinstance(box := boxes[0], dict)
    data = {"bbox": ",".join([str(box[k]) for k in ["xmin", "ymin", "xmax", "ymax"]])}
    headers = {}
    if request:  # avoid DOS - can be None despite type hint!
        client_ip = request.headers.get("x-forwarded-for") or request.client.host
        headers = {"X-HF-Client-IP": client_ip}
    with io.BytesIO() as f:
        img.save(f, format="JPEG")
        r = httpx.post(
            API_URL,
            data=data,
            files={"file": f},
            verify=CA_BUNDLE or True,
            timeout=30.0,
            auth=auth,
            headers=headers,
        )
    r.raise_for_status()

    output_image = Image.open(io.BytesIO(r.content))
    return (img, output_image)


def on_change_bbox(prompts: dict[str, Any]):
    return gr.update(interactive=len(prompts["boxes"]) > 0)


def process_prompt(
    img: Image.Image,
    prompt: str,
    request: gr.Request | None,
) -> tuple[Image.Image, Image.Image]:
    data = {"prompt": prompt}
    headers = {}
    if request:  # avoid DOS - can be None despite type hint!
        client_ip = request.headers.get("x-forwarded-for") or request.client.host
        headers = {"X-HF-Client-IP": client_ip}
    with io.BytesIO() as f:
        img.save(f, format="JPEG")
        r = httpx.post(
            API_URL,
            data=data,
            files={"file": f},
            verify=CA_BUNDLE or True,
            timeout=30.0,
            auth=auth,
            headers=headers,
        )
    r.raise_for_status()

    output_image = Image.open(io.BytesIO(r.content))
    return (img, output_image)


def on_change_prompt(img: Image.Image | None, prompt: str | None):
    return gr.update(interactive=bool(img and prompt))


TITLE = """
<center>
  <h1 style="font-size: 1.5rem; margin-bottom: 0.5rem;">
    Object Eraser Powered By Refiners
  </h1>
  <div style="
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
    font-size: 1.25rem;
    flex-wrap: wrap;
  ">
    <a href="https://github.com/finegrain-ai/refiners" target="_blank">[Refiners]</a>
    <a href="https://finegrain.ai/" target="_blank">[Finegrain]</a>
    <a
        href="https://huggingface.co/spaces/finegrain/finegrain-image-enhancer"
        target="_blank"
    >[Finegrain Image Enhancer]</a>
  </div>
  <p>
    Erase any object from your image just by naming it — no manual work required!
    Not only will the object disappear, but so will its effects on the scene, like shadows or reflections.
  </p>
  <p>
    This space is powered by Refiners, our open source micro-framework for simple foundation model adaptation.
    If you enjoyed it, please consider starring Refiners on GitHub!
  </p>
  <a href="https://github.com/finegrain-ai/refiners" target="_blank">
    <img src="https://img.shields.io/github/stars/finegrain-ai/refiners?style=social" />
  </a>
</center>
"""

with gr.Blocks() as demo:
    gr.HTML(TITLE)
    with gr.Tab("By prompt", id="tab_prompt"):
        with gr.Row():
            with gr.Column():
                iimg = gr.Image(type="pil", label="Input")
                prompt = gr.Textbox(label="What should we erase?")
            with gr.Column():
                oimg = ImageSlider(label="Output")
        with gr.Row():
            btn = gr.ClearButton(components=[oimg], value="Erase Object", interactive=False)

        for inp in [iimg, prompt]:
            inp.change(
                fn=on_change_prompt,
                inputs=[iimg, prompt],
                outputs=[btn],
            )
        btn.click(
            fn=process_prompt,
            inputs=[iimg, prompt],
            outputs=[oimg],
            api_name=False,
        )

        examples = [
            [
                "examples/white-towels-rattan-basket-white-table-with-bright-room-background.jpg",
                "soap",
            ],
            [
                "examples/interior-decor-with-mirror-potted-plant.jpg",
                "potted plant",
            ],
            [
                "examples/detail-ball-basketball-court-sunset.jpg",
                "basketball",
            ],
            [
                "examples/still-life-device-table_23-2150994394.jpg",
                "glass of water",
            ],
            [
                "examples/knife-fork-green-checkered-napkin_140725-63576.jpg",
                "knife and fork",
            ],
            [
                "examples/city-night-with-architecture-vibrant-lights_23-2149836930.jpg",
                "frontmost black car on right lane",
            ],
            [
                "examples/close-up-coffee-latte-wooden-table_23-2147893063.jpg",
                "coffee cup on plate",
            ],
            [
                "examples/empty-chair-with-vase-plant_74190-2078.jpg",
                "chair",
            ],
        ]

        ex = gr.Examples(
            examples=examples,
            inputs=[iimg, prompt],
            outputs=[oimg],
            fn=process_prompt,
            cache_examples=True,
        )
    with gr.Tab("By bounding box", id="tab_bb"):
        with gr.Row():
            with gr.Column():
                annotator = image_annotator(
                    image_type="pil",
                    disable_edit_boxes=True,
                    show_download_button=False,
                    show_share_button=False,
                    single_box=True,
                    label="Input",
                )
            with gr.Column():
                oimg = ImageSlider(label="Output")
        with gr.Row():
            btn = gr.ClearButton(components=[oimg], value="Erase Object", interactive=False)

        annotator.change(
            fn=on_change_bbox,
            inputs=[annotator],
            outputs=[btn],
        )
        btn.click(
            fn=process_bbox,
            inputs=[annotator],
            outputs=[oimg],
            api_name=False,
        )

        examples = [
            {
                "image": "examples/white-towels-rattan-basket-white-table-with-bright-room-background.jpg",
                "boxes": [{"xmin": 836, "ymin": 475, "xmax": 1125, "ymax": 1013}],
            },
            {
                "image": "examples/interior-decor-with-mirror-potted-plant.jpg",
                "boxes": [{"xmin": 47, "ymin": 907, "xmax": 397, "ymax": 1633}],
            },
            {
                "image": "examples/detail-ball-basketball-court-sunset.jpg",
                "boxes": [{"xmin": 673, "ymin": 954, "xmax": 911, "ymax": 1186}],
            },
            {
                "image": "examples/still-life-device-table_23-2150994394.jpg",
                "boxes": [{"xmin": 429, "ymin": 586, "xmax": 571, "ymax": 834}],
            },
            {
                "image": "examples/knife-fork-green-checkered-napkin_140725-63576.jpg",
                "boxes": [{"xmin": 972, "ymin": 226, "xmax": 1092, "ymax": 1023}],
            },
            {
                "image": "examples/city-night-with-architecture-vibrant-lights_23-2149836930.jpg",
                "boxes": [{"xmin": 215, "ymin": 637, "xmax": 411, "ymax": 855}],
            },
            {
                "image": "examples/close-up-coffee-latte-wooden-table_23-2147893063.jpg",
                "boxes": [{"xmin": 255, "ymin": 456, "xmax": 1080, "ymax": 1064}],
            },
            {
                "image": "examples/empty-chair-with-vase-plant_74190-2078.jpg",
                "boxes": [{"xmin": 35, "ymin": 320, "xmax": 383, "ymax": 983}],
            },
        ]

        ex = gr.Examples(
            examples=examples,
            inputs=[annotator],
            outputs=[oimg],
            fn=process_bbox,
            cache_examples=True,
        )

demo.queue(max_size=30, api_open=False)
demo.launch(show_api=False)
