"""
==========================================================
Micro-Cam
Configuration File
==========================================================
"""

from pathlib import Path

# Application

APP_NAME = "Micro-Cam"

APP_VERSION = "1.0.0"

WINDOW_TITLE = "Micro-Cam"

WINDOW_WIDTH = 1600

WINDOW_HEIGHT = 950

FULLSCREEN = False

# Camera

CAMERA_INDEX = 0

PREVIEW_WIDTH = 1920

PREVIEW_HEIGHT = 1080

PREVIEW_FORMAT = "RGB888"

PREVIEW_FPS = 30

CAPTURE_WIDTH = 9248

CAPTURE_HEIGHT = 6944

CAPTURE_FORMAT = "RGB888"

VIDEO_WIDTH = 1920

VIDEO_HEIGHT = 1080

VIDEO_FPS = 30

VIDEO_BITRATE = 10000000

# Zoom

MIN_ZOOM = 1.0

MAX_ZOOM = 10.0

DEFAULT_ZOOM = 1.0

ZOOM_STEP = 0.1

# Focus

AUTOFOCUS = True

MIN_FOCUS = 0.0

MAX_FOCUS = 10.0

DEFAULT_FOCUS = 5.0

# Exposure

DEFAULT_EXPOSURE = 0

MIN_EXPOSURE = -8

MAX_EXPOSURE = 8

# Image Controls

DEFAULT_BRIGHTNESS = 0.0

DEFAULT_CONTRAST = 1.0

DEFAULT_SATURATION = 1.0

DEFAULT_SHARPNESS = 1.0

# White Balance

DEFAULT_WHITE_BALANCE = "Auto"

WHITE_BALANCE_MODES = [

    "Auto",

    "Daylight",

    "Cloudy",

    "Indoor",

    "Fluorescent",

    "Tungsten"

]

# Image Saving

IMAGE_FORMAT = "jpg"

IMAGE_QUALITY = 100

SAVE_FULL_IMAGE = True

SAVE_ZOOM_IMAGE = True

SAVE_THUMBNAIL = True

SAVE_METADATA = True

# Video

VIDEO_EXTENSION = "mp4"

# Gallery

THUMBNAIL_SIZE = 180

MAX_RECENT_IMAGES = 200

# Upload

ENABLE_UPLOAD = True

RCLONE_REMOTE = "MicroCam"

RCLONE_FOLDER = "Captures"

DELETE_AFTER_UPLOAD = False

# Status Text

STATUS_READY = "Ready"

STATUS_CAPTURING = "Capturing..."

STATUS_RECORDING = "Recording..."

STATUS_UPLOADING = "Uploading..."

STATUS_SAVING = "Saving..."

STATUS_DONE = "Done"

STATUS_ERROR = "Error"

# Directories

BASE_DIR = Path(__file__).resolve().parent

CAPTURE_DIR = BASE_DIR / "captures"

VIDEO_DIR = BASE_DIR / "videos"

THUMBNAIL_DIR = BASE_DIR / "thumbnails"

TEMP_DIR = BASE_DIR / "temp"

ICON_DIR = BASE_DIR / "icons"

LOG_DIR = BASE_DIR / "logs"

SETTINGS_DIR = BASE_DIR / "settings"

# Create Directories

DIRECTORIES = [

    CAPTURE_DIR,

    VIDEO_DIR,

    THUMBNAIL_DIR,

    TEMP_DIR,

    ICON_DIR,

    LOG_DIR,

    SETTINGS_DIR

]

for folder in DIRECTORIES:

    folder.mkdir(

        parents=True,

        exist_ok=True

    )

# Theme

BACKGROUND_COLOR = "#202020"

TEXT_COLOR = "#FFFFFF"

BUTTON_HEIGHT = 45

BUTTON_WIDTH = 130

SLIDER_WIDTH = 250

# Logging

ENABLE_LOG = True

LOG_FILE = LOG_DIR / "microcam.log"