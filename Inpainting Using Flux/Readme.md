

# FLUX.1 Inpainting 🔥

This project showcases an inpainting model using the FLUX.1 pipeline by Black Forest Labs, enhanced for image inpainting tasks. The code enables users to remove backgrounds, apply masks, and generate high-quality inpainted images based on a text prompt.
![image](https://github.com/user-attachments/assets/0d22c816-f5fa-4010-83fe-3e1069653841)

## Overview

This project leverages the FLUX.1 inpainting model to transform images using a mask and a text-based prompt. The implementation supports GPU acceleration and provides an interactive interface for users to experiment with the inpainting process.

### Features

- **Background Removal**: Remove backgrounds from images based on a threshold value.
- **Text-based Inpainting**: Generate inpainted images using text prompts and mask overlays.
- **Adjustable Parameters**: Customize the seed, transformation strength, and number of inference steps.
- **Interactive Interface**: Use Gradio to interact with the model and visualize results.

## Dependencies

Ensure you have the following packages installed:

- `requests`
- `numpy`
- `torch`
- `PIL`
- `gradio`
- `diffusers`
- `spaces`

You can install the required packages using pip:

```bash
pip install requests numpy torch pillow gradio diffusers
```

## Usage

1. **Clone the repository:**

2. **Run the script:**



This will launch a Gradio interface where you can upload images, define text prompts, and adjust settings to generate inpainted images.

3. **Customize the inpainting process:**

- **Upload an Image**: Use the image editor to upload or capture an image and apply a mask.
- **Enter a Text Prompt**: Provide a text prompt that describes the inpainting transformation you want.
- **Adjust Settings**: Customize the seed, transformation strength, and number of inference steps to fine-tune the result.

4. **View the Results**: The generated image will be displayed along with the input mask for comparison.

## Example Inputs

You can explore some predefined examples by running the script, which will provide default inputs and prompts for testing.

## Acknowledgments

- **Black Forest Labs** for creating the FLUX.1 model.
- **Gothos** for enhancing the model with inpainting capabilities.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



---

```

