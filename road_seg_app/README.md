# Road Segmentation Analysis System

A web-based major project that detects road regions in uploaded images and estimates road coverage percentage using image-processing techniques.

## Project Overview

This project is designed as a practical computer vision application where a user uploads a road image, and the system processes it to identify road-like pixels and highlight the detected road region in the output image. The result includes important metrics such as road pixel count and coverage percentage.

## Objective

To build a simple yet effective road segmentation system that can:
- allow image upload from the browser
- process the uploaded image on the backend
- detect road areas using threshold-based segmentation
- produce an annotated output image
- display analysis results to the user

## Features

- Separate backend and frontend architecture
- Flask-based REST API
- Image upload and processing
- Road region detection using adaptive brightness and color-based conditions
- Coverage estimation in percentage
- Output image generation with overlay highlighting
- Simple web-based dashboard interface

## Tech Stack

- Python
- Flask
- Flask-CORS
- Pillow
- NumPy
- HTML
- CSS
- JavaScript

## Project Structure

- Backend/
  - app.py
  - requirements.txt
  - output/
- Frontend/
  - index.html
  - styles.css
  - script.js
- README.md

## Backend Setup

1. Open a terminal in the Backend folder.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the backend server:

```bash
python app.py
```

The backend runs at:
- http://localhost:5000

## Frontend Setup

Open the Frontend/index.html file in a browser.

If needed, you can also use a simple local web server for better compatibility.

## API Endpoints

- GET /api/health
- GET /api/project
- POST /api/analyze
- GET /api/output/<filename>

## Usage

1. Launch the backend server.
2. Open the frontend page in the browser.
3. Upload a road image.
4. Click "Analyze Image".
5. View the segmented output and metrics such as:
   - road pixels
   - coverage percentage
   - confidence score

## Verification Evidence

The project was validated with a real backend smoke test using Flask's test client.

Command used:

```bash
cd /d "C:\Users\Asus\Downloads\road_seg_app\Backend" && python -c "import json; from io import BytesIO; from PIL import Image; from app import app; c=app.test_client(); h=c.get('/api/health'); img=Image.new('RGB',(200,150), color=(20,30,40)); b=BytesIO(); img.save(b, format='PNG'); b.seek(0); r=c.post('/api/analyze', data={'image': (b,'road.png')}, content_type='multipart/form-data'); print(json.dumps({'health_status': h.status_code, 'health_json': h.get_json(), 'analyze_status': r.status_code, 'analyze_json': r.get_json()}, default=str))"
```

Observed outcome:
- health endpoint returned success status
- image analysis endpoint returned success status
- valid JSON response was generated

This confirms the backend is responding successfully and the analysis route is functional for uploaded images.

## Submission Guidance

Before final submission, discuss the project with your Project Guide and confirm the required evaluation format. Prepare the following:

- GitHub repository link
- Google Drive link for screenshots and demo videos
- Demo video or screen recording of the application
- Output images or result screenshots
- Project report / PPT if required by the institution

## Important Note

This is a working prototype and proof-of-concept road segmentation system built using image-processing logic. It demonstrates the core functionality and architecture clearly, but it should be presented honestly as an implemented prototype with validated backend behavior.

## Conclusion

This project demonstrates a complete end-to-end workflow for road segmentation analysis, from image upload to result visualization, and can be used as a strong academic major-project foundation.
