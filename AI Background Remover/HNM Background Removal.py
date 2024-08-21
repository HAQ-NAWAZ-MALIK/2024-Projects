import gradio as gr
from gradio_imageslider import ImageSlider
from loadimg import load_img
import spaces
from transformers import AutoModelForImageSegmentation
import torch
from torchvision import transforms

torch.set_float32_matmul_precision(["high", "highest"][0])

# Load the BiRefNet model for image segmentation
birefnet = AutoModelForImageSegmentation.from_pretrained(
    "ZhengPeng7/BiRefNet", trust_remote_code=True
)
birefnet.to("cuda")

# Define image transformation steps
transform_image = transforms.Compose(
    [
        transforms.Resize((1024, 1024)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)

@spaces.GPU
def process_image(image):
    im = load_img(image, output_type="pil")
    im = im.convert("RGB")
    image_size = im.size
    original_image = im.copy()
    image = load_img(im)
    input_images = transform_image(image).unsqueeze(0).to("cuda")
    # Perform prediction
    with torch.no_grad():
        predictions = birefnet(input_images)[-1].sigmoid().cpu()
    prediction = predictions[0].squeeze()
    prediction_pil = transforms.ToPILImage()(prediction)
    mask = prediction_pil.resize(image_size)
    image.putalpha(mask)
    return (image, original_image)

# Create Gradio image sliders
slider1 = ImageSlider(label="BiRefNet Output", type="pil")
slider2 = ImageSlider(label="BiRefNet Output", type="pil")

# Define Gradio inputs and outputs
image_input = gr.Image(label="Upload an image")
url_input = gr.Textbox(label="Paste an image URL")

# Example images
chameleon = load_img("/content/ElonMusk.jpg", output_type="pil")
url_example = "https://hips.hearstapps.com/hmg-prod/images/gettyimages-1229892983-square.jpg"

# Create Gradio interfaces
interface1 = gr.Interface(
    process_image, inputs=image_input, outputs=slider1, examples=[chameleon], api_name="image"
)

interface2 = gr.Interface(
    process_image, inputs=url_input, outputs=slider2, examples=[url_example], api_name="text"
)

# Create a tabbed Gradio interface
demo = gr.TabbedInterface(
    [interface1, interface2], ["Image", "Text"], title="HNM Background Removal"
)

if __name__ == "__main__":
    demo.launch()
