# Object Eraser Powered by Refiners

Object Eraser is a powerful tool that allows you to easily remove objects from your images by simply naming them or by selecting a bounding box. The tool handles the entire process, ensuring that the object is not only removed but that any effects it had on the scene, such as shadows or reflections, are also seamlessly erased.

This project leverages Refiners, an open-source micro-framework designed for the simple adaptation of foundation models, to deliver a user-friendly and efficient image editing experience.

## Features

- **Erase by Prompt:** Simply type the name of the object you want to remove, and the tool will handle the rest.
- **Erase by Bounding Box:** Draw a bounding box around the object you want to remove for a more precise selection.
- **Interactive UI:** The Gradio interface provides an intuitive, easy-to-use platform with real-time updates.
- **Powered by Refiners:** Utilizes the Refiners framework for efficient model adaptation and processing.
- **Seamless Integration:** Works with various image types and handles complex scenes, ensuring a smooth erasure process.

## How It Works

### 1. Erase by Prompt
- Upload your image.
- Enter a description of the object you wish to remove in the prompt textbox.
- Click the "Erase Object" button to see the magic happen.

### 2. Erase by Bounding Box
- Upload your image.
- Use the bounding box tool to select the object you want to remove.
- Click the "Erase Object" button to see the results.

## Examples

Here are some example scenarios where the Object Eraser has been used effectively:

- **Soap removed from a clean room setting**  
  ![Before](examples/white-towels-rattan-basket-white-table-with-bright-room-background.jpg)  
  ![After](examples/white-towels-rattan-basket-white-table-with-bright-room-background.jpg)

- **Potted plant removed from a mirror reflection**  
  ![Before](examples/interior-decor-with-mirror-potted-plant.jpg)  
  ![After](examples/interior-decor-with-mirror-potted-plant.jpg)

- **Basketball removed from a court**  
  ![Before](examples/detail-ball-basketball-court-sunset.jpg)  
  ![After](examples/detail-ball-basketball-court-sunset.jpg)

For more examples, check the examples folder.

## Getting Started

### Prerequisites

- Python 3.7+
- Gradio
- PIL
- httpx
- environs

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/object-eraser.git
   cd object-eraser
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:

   Create a `.env` file in the root directory and add the following:

   ```env
   ERASER_API_URL="https://spaces.finegrain.ai/eraser"
   ERASER_API_KEY="your_api_key"
   ERASER_CA_BUNDLE="path_to_ca_bundle"
   ```

4. Run the application:

   ```bash
   python app.py
   ```

### Usage

Once the application is running, you can access it through your browser. The interface will allow you to upload images, either enter a prompt or select a bounding box, and erase the desired objects.

## Contributing

We welcome contributions! If you have suggestions, find a bug, or want to add new features, please fork the repository and create a pull request. 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Gradio](https://gradio.app/)
- [Refiners Framework](https://github.com/finegrain-ai/refiners)
- [Hugging Face](https://huggingface.co/)
- [PIL](https://pillow.readthedocs.io/en/stable/)

---

If you enjoyed using Object Eraser, please consider starring [Refiners on GitHub](https://github.com/finegrain-ai/refiners)!
