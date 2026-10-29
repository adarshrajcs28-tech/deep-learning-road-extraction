const form = document.getElementById('uploadForm');
const imageInput = document.getElementById('imageInput');
const statusBox = document.getElementById('status');
const originalImage = document.getElementById('originalImage');
const segmentedImage = document.getElementById('segmentedImage');
const roadPixels = document.getElementById('roadPixels');
const coverage = document.getElementById('coverage');
const confidence = document.getElementById('confidence');
const imageSize = document.getElementById('imageSize');

function setDefaultState() {
  roadPixels.textContent = '0';
  coverage.textContent = '0%';
  confidence.textContent = '0%';
  imageSize.textContent = '0 × 0';
  originalImage.src = '';
  segmentedImage.src = '';
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const file = imageInput.files[0];
  if (!file) {
    statusBox.textContent = 'Please select an image first.';
    return;
  }

  statusBox.textContent = 'Analyzing road image...';

  const formData = new FormData();
  formData.append('image', file);

  try {
    const response = await fetch('http://localhost:5000/api/analyze', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Analysis failed.');
    }

    originalImage.src = `http://localhost:5000${data.original_image}`;
    segmentedImage.src = `http://localhost:5000${data.output_image}`;

    roadPixels.textContent = data.road_pixels.toLocaleString();
    coverage.textContent = `${data.coverage_percent}%`;
    confidence.textContent = `${data.confidence}%`;
    imageSize.textContent = `${data.image_size.width} × ${data.image_size.height}`;

    statusBox.textContent = `${data.message} Confidence: ${data.confidence}%`;
  } catch (error) {
    statusBox.textContent = error.message;
  }
});

setDefaultState();
