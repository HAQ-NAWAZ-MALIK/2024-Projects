# Virtual Try-On Web Application

This web application allows users to virtually try on garments by uploading images of a person and a garment. It uses a machine learning model {Kwai-Kolors/Model} to generate a realistic composite image of the person wearing the selected garment.

## Features

- Upload or select from example images for both person and garment
- Generate virtual try-on results with a single click
- Adjustable seed for result variation
- Random seed option for diverse outputs
- Showcase of example try-on results

## Installation

1. Clone this repository
2. Install the required dependencies:
```
pip install opencv-python pillow gradio numpy requests

```


3. Set up the following environment variables:
- `tryon_url`: URL of the try-on API
- `token`: Authentication token for the API
- `Cookie`: Cookie value for API requests
- `referer`: Referer value for API requests

## Usage

Then open a web browser and navigate to the URL displayed in the console (typically `http://localhost:7860`).

## How it works

1. Upload or select a person image and a garment image
2. Click the "Run" button
3. The application will send the images to the try-on API
4. After processing, the result image will be displayed

You can adjust the seed value or use a random seed for different variations of the result.

## API

The application uses two main functions:

- `tryon()`: Sends images to the API and retrieves results asynchronously
- `start_tryon()`: Sends images to the API and waits for the result (currently commented out)

## Limitations

- The application is rate-limited and may return errors if too many users are accessing it simultaneously
- Processing time may vary depending on server load and image complexity



Run the application:
---
title: Kolors Virtual Try-On
emoji: 👕
colorFrom: purple
colorTo: gray
sdk: gradio
sdk_version: 4.38.1
app_file: app.py
pinned: false
license: apache-2.0
---



Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
