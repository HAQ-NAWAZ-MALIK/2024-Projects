# Background Removal with BiRefNet
![image](https://github.com/user-attachments/assets/5e2b8b4f-c1f8-4be0-bace-5d244b98b5c0)

This project implements an image segmentation application using the BiRefNet model. The application allows users to upload images or provide image URLs, processes the images to remove backgrounds, and displays the results using Gradio interfaces.

## Features

- **Image Upload**: Upload an image to remove its background.
- **Image URL**: Paste a URL to process an image directly from the web.
- **Image Segmentation**: Uses the BiRefNet model for background removal.
## NOTE 
This Project Works on GPU

Code Explanation
Model Loading: AutoModelForImageSegmentation is used to load the BiRefNet model for image segmentation.
Image Transformation: The transform_image function applies resizing, normalization, and tensor conversion to the input image.
Image Processing: process_image(image) handles loading, transforming, predicting, and applying the segmentation mask to the uploaded image.
Gradio Interfaces:
interface1: For uploading images.
interface2: For pasting image URLs.
Tabbed Interface: gr.TabbedInterface combines the two interfaces into a single tabbed layout.
