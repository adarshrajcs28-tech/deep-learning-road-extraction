from datetime import datetime
from pathlib import Path

import numpy as np
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from PIL import Image

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


@app.get("/")
def home():
    return jsonify({
        "project": "Road Segmentation System",
        "status": "running",
        "description": "AI-assisted road extraction and area coverage analysis for road images.",
        "routes": [
            "/api/health",
            "/api/project",
            "/api/analyze"
        ]
    })


@app.get("/api/health")
def health_check():
    return jsonify({
        "status": "ok",
        "message": "Backend is running successfully.",
        "service": "road-segmentation-api"
    })


@app.get("/api/project")
def project_info():
    return jsonify({
        "title": "Road Segmentation Analysis System",
        "category": "Computer Vision / Image Processing",
        "objective": "Detect road regions in uploaded images and estimate total road coverage.",
        "modules": [
            "Image upload and preprocessing",
            "Road pixel extraction",
            "Coverage estimation",
            "Result visualization"
        ]
    })


@app.post("/api/analyze")
def analyze_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded."}), 400

    uploaded_file = request.files["image"]
    if uploaded_file.filename == "":
        return jsonify({"error": "No selected file."}), 400

    try:
        image = Image.open(uploaded_file.stream).convert("RGB")
    except Exception:
        return jsonify({"error": "Invalid image file. Please upload a PNG, JPG, or JPEG image."}), 400

    original_width, original_height = image.size
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_name = f"original_{timestamp}.png"
    output_name = f"segmented_{timestamp}.png"

    original_path = OUTPUT_DIR / original_name
    image.save(original_path)

    analysis = compute_road_segmentation(image)
    annotated = create_overlay(image, analysis["mask"])
    annotated_path = OUTPUT_DIR / output_name
    annotated.save(annotated_path)

    return jsonify({
        "status": "success",
        "message": "Road segmentation analysis completed successfully.",
        "project": "Road Segmentation System",
        "image_size": {"width": original_width, "height": original_height},
        "road_pixels": int(analysis["road_pixels"]),
        "coverage_percent": round(analysis["coverage_percent"], 2),
        "road_density": round(analysis["road_density"], 2),
        "confidence": round(analysis["confidence"], 2),
        "method": "adaptive brightness threshold + morphological smoothing",
        "output_image": f"/api/output/{output_name}",
        "original_image": f"/api/output/{original_name}"
    })


@app.get("/api/output/<filename>")
def send_output(filename):
    return send_from_directory(OUTPUT_DIR, filename)


def compute_road_segmentation(image: Image.Image):
    arr = np.array(image.convert("RGB"))
    height, width, _ = arr.shape

    lower_half = arr[int(height * 0.25):]
    red = lower_half[:, :, 0].astype(np.float32)
    green = lower_half[:, :, 1].astype(np.float32)
    blue = lower_half[:, :, 2].astype(np.float32)

    brightness = (red + green + blue) / 3.0
    is_road = (
        (brightness < 200)
        & (red > 30)
        & (green > 25)
        & (blue > 20)
    ) | (
        (red > green)
        & (red > blue)
        & (brightness < 220)
    )

    mask = np.zeros((height, width), dtype=np.uint8)
    mask[int(height * 0.25):] = np.where(is_road, 255, 0).astype(np.uint8)

    cleaned = mask.copy()
    for _ in range(2):
        cleaned = morphological_dilate(cleaned)

    road_pixels = int(np.sum(cleaned > 0))
    total_pixels = max(1, height * width)
    coverage_percent = (road_pixels / total_pixels) * 100
    road_density = (road_pixels / max(1, np.count_nonzero(cleaned >= 128))) * 100 if np.any(cleaned >= 128) else 0
    confidence = min(100.0, max(0.0, coverage_percent * 0.9 + road_density * 0.1))

    return {
        "mask": cleaned,
        "road_pixels": road_pixels,
        "coverage_percent": coverage_percent,
        "road_density": road_density,
        "confidence": confidence,
    }


def morphological_dilate(mask: np.ndarray) -> np.ndarray:
    result = mask.copy()
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            shifted = np.roll(mask, shift=(dy, dx), axis=(0, 1))
            result = np.maximum(result, shifted)
    return result


def create_overlay(image: Image.Image, mask: np.ndarray) -> Image.Image:
    rgba = image.convert("RGBA")
    rgba_array = np.array(rgba)

    red = rgba_array[:, :, 0]
    green = rgba_array[:, :, 1]
    blue = rgba_array[:, :, 2]
    alpha = rgba_array[:, :, 3]

    road_mask = mask > 128
    red[road_mask] = np.clip(red[road_mask] * 0.7 + 80, 0, 255)
    green[road_mask] = np.clip(green[road_mask] * 0.8 + 60, 0, 255)
    blue[road_mask] = np.clip(blue[road_mask] * 0.9 + 95, 0, 255)
    alpha[road_mask] = 220

    rgba_array[:, :, 0] = red
    rgba_array[:, :, 1] = green
    rgba_array[:, :, 2] = blue
    rgba_array[:, :, 3] = alpha

    return Image.fromarray(rgba_array, mode="RGBA")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
