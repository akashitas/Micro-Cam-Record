# Micro-Cam – Raspberry Pi 5 Arducam 64MP Camera System

**Micro-Cam** is a Raspberry Pi 5 based camera system developed using the **Arducam 64MP OV64A40 camera**, **Picamera2**, **libcamera**, **OpenCV**, and Python.

The project provides a complete camera engine for high-resolution photography, live preview, autofocus, manual camera controls, digital zoom processing, metadata generation, thumbnails, and H.264 video recording.

## Hardware

* Raspberry Pi 5
* Arducam 64MP OV64A40 Camera
* Camera interface cable
* MicroSD card
* Raspberry Pi power supply

## Software

* Python 3
* Raspberry Pi OS
* Picamera2
* libcamera
* OpenCV
* NumPy

## Key Features

### Camera Management

* Camera initialization
* Camera start/stop
* Camera restart
* Camera availability detection
* Camera model identification
* Sensor size detection
* Camera information and control information

### Image Capture

* Full-resolution image capture
* Automatic autofocus before capture
* Timestamp-based image naming
* Event-based capture folders
* JPEG image storage

### Image Processing

* Thumbnail generation
* Digital zoom image generation
* OpenCV image processing
* Cubic interpolation for zoomed images

### Camera Controls

* Continuous autofocus
* Single autofocus
* Manual focus
* Zoom control
* Exposure compensation
* Brightness
* Contrast
* Saturation
* Sharpness
* Automatic white balance
* Manual white balance
* Analogue gain / ISO
* Reset camera controls

### Metadata

Each captured image can have associated JSON metadata containing information such as:

* Capture time
* Camera model
* Image width
* Image height
* Zoom level
* Focus value

### Video Recording

The camera engine supports video recording using:

* H264Encoder
* FileOutput
* Configurable video bitrate
* MP4 output

### Live Preview

OpenCV is used to display a live camera preview.

Keyboard controls in the test interface:

```text
C → Capture photograph
V → Start/stop video recording
Q → Quit
```

---

# System Architecture

```text
                    ┌──────────────────────┐
                    │      Raspberry Pi 5  │
                    │                      │
                    │       Python         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Camera Engine   │
                    │      Python Class    │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌───────────┐    ┌───────────┐    ┌───────────┐
        │ Picamera2 │    │ OpenCV    │    │ libcamera │
        └─────┬─────┘    └─────┬─────┘    └─────┬─────┘
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Arducam OV64A40      │
                    │       64MP Camera    │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
         Photographs        Preview          Video
              │                │                │
              ▼                ▼                ▼
         JPEG + JSON       OpenCV GUI        H.264/MP4
              │
       ┌──────┴────────┐
       ▼               ▼
   Thumbnail       Zoom Image
```

# Project Workflow

```text
             Start Micro-Cam
                    │
                    ▼
          Initialize Camera
                    │
                    ▼
             Start Preview
                    │
                    ▼
          Continuous Autofocus
                    │
                    ▼
             Live Preview
                    │
       ┌────────────┼────────────┐
       │            │            │
       ▼            ▼            ▼
      'C'          'V'          'Q'
       │            │            │
       ▼            ▼            ▼
    Capture       Video        Exit
     Photo       Recording       │
       │            │            ▼
       │            │       Close Camera
       │            │
       ▼            ▼
    Process       Start/Stop
     Image        Recording
       │
       ├───────────────┐
       │               │
       ▼               ▼
  Thumbnail       Zoom Image
       │
       └───────┬───────┘
               ▼
          JSON Metadata
```

# Camera Configuration

The camera engine creates three camera configurations:

```text
Preview Configuration
        ↓
Live camera preview

Capture Configuration
        ↓
High-resolution photographs

Video Configuration
        ↓
Video recording
```

The project stores these configurations as:

```python
self.preview_config
self.capture_config
self.video_config
```

The camera sensor size is also obtained from the camera properties.

# Autofocus

The system supports two autofocus modes.

## Continuous Autofocus

Continuous autofocus is enabled when the camera starts:

```python
AfMode = Continuous
```

This allows the camera to continuously adjust focus during normal operation.

## Single Autofocus

Single autofocus can be triggered manually:

```python
AfMode = Auto
AfTrigger = Start
```

This is used before capturing photographs.

# Manual Focus

The user can manually control lens focus.

The requested focus value is converted to a floating-point value and constrained between the configured minimum and maximum focus values.

```text
User Focus Value
       ↓
Convert to Float
       ↓
Apply Min/Max Limits
       ↓
Manual Focus Mode
       ↓
Set Lens Position
```

# Digital Zoom

The system implements zoom by modifying the camera's `ScalerCrop` control.

```text
Sensor Image
     ↓
Calculate Crop Region
     ↓
Center Crop
     ↓
ScalerCrop
     ↓
Zoomed Preview
```

The zoom value is limited between configured minimum and maximum values.

The system also supports saving a zoomed version of a captured image using OpenCV.

# Exposure and Image Controls

The camera engine provides software controls for:

```text
Exposure
Brightness
Contrast
Saturation
Sharpness
ISO / Analogue Gain
```

These controls can be modified during operation.

# White Balance

Two white-balance modes are available.

### Automatic White Balance

The camera enables:

```python
AwbEnable = True
AeEnable = True
```

### Manual White Balance

Manual red and blue gains can be supplied using:

```python
set_white_balance(red_gain, blue_gain)
```

# Complete Photo Capture

The complete capture operation performs multiple processing steps.

```text
Capture Request
      ↓
Create Capture Directory
      ↓
Create Event Folder
      ↓
Generate Filename
      ↓
Autofocus
      ↓
Capture Full Resolution Image
      ↓
Return to Preview
      ↓
Create Thumbnail
      ↓
Create Zoom Image
      ↓
Save JSON Metadata
      ↓
Return Capture Information
```

The `capture_complete()` function returns:

```python
{
    "image": image,
    "thumbnail": thumbnail,
    "zoom": zoom,
    "metadata": metadata
}
```

# Thumbnail Generation

OpenCV is used to read the captured image and resize it to the configured thumbnail size.

The thumbnail is saved using the suffix:

```text
_thumb.jpg
```

Example:

```text
20260914_230000.jpg
20260914_230000_thumb.jpg
```

# Zoom Image Generation

When zoom is greater than 1×, the system calculates a centered crop from the captured image and resizes the crop back to the original image dimensions.

The resulting file uses:

```text
_zoom.jpg
```

# Metadata

A JSON file is generated for captured images.

Example structure:

```json
{
    "time": "YYYY-MM-DD HH:MM:SS",
    "camera": "Arducam OV64A40",
    "width": 0000,
    "height": 0000,
    "zoom": 1.0,
    "focus": 0.0
}
```

The exact resolution values are controlled through `config.py`.

# Video Recording

The project uses the Picamera2 H.264 encoder for video recording.

```text
Start Recording
       ↓
Create Video Directory
       ↓
Generate Filename
       ↓
Initialize H264Encoder
       ↓
Create FileOutput
       ↓
Start Encoder
       ↓
Save MP4
```

Video files are generated with timestamp-based filenames.

# OpenCV Preview

The test section continuously reads camera frames and displays them using:

```python
cv2.imshow("Micro-Cam Preview", frame)
```

This provides a real-time preview interface.

# Keyboard Controls

| Key | Function           |
| --- | ------------------ |
| C   | Capture photograph |
| V   | Start/stop video   |
| Q   | Quit application   |

# Project Structure

Recommended GitHub repository structure:

```text
micro-cam-rpi5-arducam-64mp/
│
├── README.md
├── camera.py
├── config.py
├── utils.py
├── main.py
├── requirements.txt
├── .gitignore
│
├── captures/
│   ├── images/
│   └── videos/
│
├── docs/
│   └── system_architecture.png
│
└── examples/
    └── sample_capture.jpg
```

# Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/micro-cam-rpi5-arducam-64mp.git
```

Enter the project directory:

```bash
cd micro-cam-rpi5-arducam-64mp
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Make sure Picamera2 and libcamera are installed and configured on Raspberry Pi OS.

# Requirements

```text
picamera2
opencv-python
numpy
```

The project also depends on the Raspberry Pi camera stack and the local project modules:

```text
config.py
utils.py
```

# Basic Usage

```python
from camera import Camera

camera = Camera()

camera.start()

print("Camera:", camera.camera_name())
print("Sensor:", camera.get_sensor_size())

while True:

    frame = camera.get_frame()

    # Process frame using OpenCV
    # ...

camera.close()
```

# Capture Photo

```python
filename = camera.capture_photo()

print("Captured:", filename)
```

# Complete Capture

```python
result = camera.capture_complete()

print(result)
```

The result contains the paths for:

* Original image
* Thumbnail
* Zoom image
* Metadata JSON

# Video Recording

Start recording:

```python
camera.start_recording()
```

Stop recording:

```python
camera.stop_recording()
```

# Applications

Micro-Cam can serve as a foundation for:

* High-resolution imaging
* Computer vision
* Machine vision
* AI-based inspection
* Automated photography
* Remote monitoring
* Raspberry Pi surveillance systems
* Object detection
* Image classification
* Industrial inspection
* IoT camera systems
* Research and development

# Future Development

Possible future improvements include:

* Automatic Google Drive upload
* MQTT-based remote control
* Web-based camera dashboard
* Remote image and video monitoring
* YOLO object detection
* AI-based image classification
* Automatic event detection
* Cloud storage integration
* Mobile application control
* Automatic timestamp and event organization
* Servo motor integration
* Remote camera configuration

# Author

**Shiva Kumar**

Electronics and Communication Engineering

# License

This project is intended for educational, research and development purposes.
