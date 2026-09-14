"""
==========================================================
Micro-Cam
Camera Engine
Raspberry Pi 5
Arducam 64MP OV64A40
==========================================================
"""

import os
import cv2
import time
import json
import numpy as np

from pathlib import Path

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

from libcamera import controls

from config import *
from utils import create_event_folder

from utils import image_filename

from utils import video_filename

class Camera:

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(

        self,

        camera_index=CAMERA_INDEX

    ):

        self.camera_index = camera_index

        self.picam2 = Picamera2(

            camera_index

        )

        self.running = False

        self.recording = False

        self.zoom = DEFAULT_ZOOM

        self.focus = DEFAULT_FOCUS

        self.last_frame = None

        self.sensor_size = None

        self.encoder = None

        self.output = None

        self.video_path = None

        self.preview_config = None

        self.capture_config = None

        self.video_config = None

        self.build_camera()

    # ==========================================================
    # Build Camera
    # ==========================================================

    def build_camera(

        self

    ):

        self.preview_config = self.picam2.create_preview_configuration(

            main={

                "size":

                (

                    PREVIEW_WIDTH,

                    PREVIEW_HEIGHT

                ),

                "format":

                PREVIEW_FORMAT

            },

            buffer_count=4

        )

        self.capture_config = self.picam2.create_still_configuration(

            main={

                "size":

                (

                    CAPTURE_WIDTH,

                    CAPTURE_HEIGHT

                ),

                "format":

                CAPTURE_FORMAT

            }

        )

        self.video_config = self.picam2.create_video_configuration(

            main={

                "size":

                (

                    VIDEO_WIDTH,

                    VIDEO_HEIGHT

                ),

                "format":

                PREVIEW_FORMAT

            }

        )

        self.picam2.configure(

            self.preview_config

        )

        self.sensor_size = self.picam2.camera_properties.get(

            "PixelArraySize"

        )

    # ==========================================================
    # Start Camera
    # ==========================================================

    def start(

        self

    ):

        if self.running:

            return

        self.picam2.start()

        time.sleep(

            2

        )

        self.running = True

        self.enable_continuous_autofocus()

    # ==========================================================
    # Stop Camera
    # ==========================================================

    def stop(

        self

    ):

        if not self.running:

            return

        self.picam2.stop()

        self.running = False

    # ==========================================================
    # Running
    # ==========================================================

    def is_running(

        self

    ):

        return self.running

    # ==========================================================
    # Preview Frame
    # ==========================================================

    def get_frame(

        self

    ):

        if not self.running:

            return None

        try:

            frame = self.picam2.capture_array()

            print(

                "Shape:",

                frame.shape,

                "Type:",

                frame.dtype

            )

            self.last_frame = frame

            return frame

        except Exception as e:

            print(

                "Preview Error:",

                e

            )

            return None

    # ==========================================================
    # Last Frame
    # ==========================================================

    def get_last_frame(

        self

    ):

        return self.last_frame

    # ==========================================================
    # Camera Information
    # ==========================================================

    def camera_information(

        self

    ):

        return self.picam2.camera_properties

    # ==========================================================
    # Camera Controls
    # ==========================================================

    def camera_controls(

        self

    ):

        return self.picam2.camera_controls

    # ==========================================================
    # Sensor Size
    # ==========================================================

    def get_sensor_size(

        self

    ):

        return self.sensor_size
    # ==========================================================
    # Enable Continuous Autofocus
    # ==========================================================

    def enable_continuous_autofocus(

        self

    ):

        try:

            self.picam2.set_controls(

                {

                    "AfMode":

                    controls.AfModeEnum.Continuous

                }

            )

        except Exception as e:

            print(

                "Continuous AF Error:",

                e

            )

    # ==========================================================
    # Single Autofocus
    # ==========================================================

    def autofocus(

        self

    ):

        try:

            self.picam2.set_controls(

                {

                    "AfMode":

                    controls.AfModeEnum.Auto,

                    "AfTrigger":

                    controls.AfTriggerEnum.Start

                }

            )

        except Exception as e:

            print(

                "Autofocus Error:",

                e

            )

    # ==========================================================
    # Manual Focus
    # ==========================================================

    def set_focus(

        self,

        value

    ):

        try:

            value = float(

                value

            )

            value = max(

                MIN_FOCUS,

                min(

                    MAX_FOCUS,

                    value

                )

            )

            self.focus = value

            self.picam2.set_controls(

                {

                    "AfMode":

                    controls.AfModeEnum.Manual,

                    "LensPosition":

                    value

                }

            )

        except Exception as e:

            print(

                "Focus Error:",

                e

            )

    # ==========================================================
    # Current Focus
    # ==========================================================

    def get_focus(

        self

    ):

        return self.focus

    # ==========================================================
    # Zoom
    # ==========================================================

    def set_zoom(

        self,

        zoom

    ):

        if self.sensor_size is None:

            return

        zoom = float(

            zoom

        )

        zoom = max(

            MIN_ZOOM,

            min(

                MAX_ZOOM,

                zoom

            )

        )

        self.zoom = zoom

        sensor_width = self.sensor_size[0]

        sensor_height = self.sensor_size[1]

        crop_width = int(

            sensor_width / zoom

        )

        crop_height = int(

            sensor_height / zoom

        )

        crop_x = (

            sensor_width - crop_width

        ) // 2

        crop_y = (

            sensor_height - crop_height

        ) // 2

        try:

            self.picam2.set_controls(

                {

                    "ScalerCrop":

                    (

                        crop_x,

                        crop_y,

                        crop_width,

                        crop_height

                    )

                }

            )

        except Exception as e:

            print(

                "Zoom Error:",

                e

            )

    # ==========================================================
    # Current Zoom
    # ==========================================================

    def get_zoom(

        self

    ):

        return self.zoom

    # ==========================================================
    # Reset Zoom
    # ==========================================================

    def reset_zoom(

        self

    ):

        self.set_zoom(

            DEFAULT_ZOOM

        )

    # ==========================================================
    # Lens Position
    # ==========================================================

    def lens_position(

        self

    ):

        try:

            metadata = self.picam2.capture_metadata()

            return metadata.get(

                "LensPosition",

                0

            )

        except:

            return 0
    # ==========================================================
    # Exposure Compensation
    # ==========================================================

    def set_exposure(

        self,

        value

    ):

        try:

            value = max(

                MIN_EXPOSURE,

                min(

                    MAX_EXPOSURE,

                    float(

                        value

                    )

                )

            )

            self.picam2.set_controls(

                {

                    "ExposureValue":

                    value

                }

            )

        except Exception as e:

            print(

                "Exposure Error:",

                e

            )

    # ==========================================================
    # Brightness
    # ==========================================================

    def set_brightness(

        self,

        value

    ):

        try:

            self.picam2.set_controls(

                {

                    "Brightness":

                    float(

                        value

                    )

                }

            )

        except Exception as e:

            print(

                "Brightness Error:",

                e

            )

    # ==========================================================
    # Contrast
    # ==========================================================

    def set_contrast(

        self,

        value

    ):

        try:

            self.picam2.set_controls(

                {

                    "Contrast":

                    float(

                        value

                    )

                }

            )

        except Exception as e:

            print(

                "Contrast Error:",

                e

            )

    # ==========================================================
    # Saturation
    # ==========================================================

    def set_saturation(

        self,

        value

    ):

        try:

            self.picam2.set_controls(

                {

                    "Saturation":

                    float(

                        value

                    )

                }

            )

        except Exception as e:

            print(

                "Saturation Error:",

                e

            )

    # ==========================================================
    # Sharpness
    # ==========================================================

    def set_sharpness(

        self,

        value

    ):

        try:

            self.picam2.set_controls(

                {

                    "Sharpness":

                    float(

                        value

                    )

                }

            )

        except Exception as e:

            print(

                "Sharpness Error:",

                e

            )

    # ==========================================================
    # Auto White Balance
    # ==========================================================

    def enable_auto_white_balance(

        self

    ):

        try:

            self.picam2.set_controls(

                {

                    "AwbEnable":True,
                    "AeEnable": True

                }

            )

        except Exception as e:

            print(

                "AWB Error:",

                e

            )

    # ==========================================================
    # Manual White Balance
    # ==========================================================

    def set_white_balance(

        self,

        red_gain,

        blue_gain

    ):

        try:

            self.picam2.set_controls(

                {

                    "AwbEnable":

                    False,

                    "ColourGains":

                    (

                        float(red_gain),

                        float(blue_gain)

                    )

                }

            )

        except Exception as e:

            print(

                "White Balance Error:",

                e

            )

    # ==========================================================
    # ISO / Analogue Gain
    # ==========================================================

    def set_iso(

        self,

        gain

    ):

        try:

            self.picam2.set_controls(

                {

                    "AnalogueGain":

                    float(

                        gain

                    )

                }

            )

        except Exception as e:

            print(

                "ISO Error:",

                e

            )

    # ==========================================================
    # Reset Camera Controls
    # ==========================================================

    def reset_controls(

        self

    ):

        self.set_zoom(

            DEFAULT_ZOOM

        )

        self.set_focus(

            DEFAULT_FOCUS

        )

        self.set_exposure(

            DEFAULT_EXPOSURE

        )

        self.set_brightness(

            DEFAULT_BRIGHTNESS

        )

        self.set_contrast(

            DEFAULT_CONTRAST

        )

        self.set_saturation(

            DEFAULT_SATURATION

        )

        self.set_sharpness(

            DEFAULT_SHARPNESS

        )

        self.enable_auto_white_balance()
    # ==========================================================
    # Capture Directory
    # ==========================================================

    def create_capture_directory(

        self

    ):

        Path(

            CAPTURE_DIR

        ).mkdir(

            parents=True,

            exist_ok=True

        )

    # ==========================================================
    # Image Name
    # ==========================================================

    def create_image_name(

        self

    ):

        return time.strftime(

            "%Y%m%d_%H%M%S"

        )

    # ==========================================================
    # Capture Full Resolution Image
    # ==========================================================

    def capture_photo(

        self

    ):

        try:

            self.create_capture_directory()

            event_folder = create_event_folder()

            filename = image_filename()

            self.autofocus()

            time.sleep(

                0.4

            )

            self.picam2.switch_mode_and_capture_file(

                self.capture_config,

                filename

            )

            self.picam2.switch_mode(

                self.preview_config

            )

            self.enable_continuous_autofocus()

            return filename

        except Exception as e:

            print(

                "Capture Error:",

                e

            )

            return None
    # ==========================================================
    # Thumbnail
    # ==========================================================

    def create_thumbnail(

        self,

        image_path

    ):

        try:

            image = cv2.imread(

                image_path

            )

            thumb = cv2.resize(

                image,

                (

                    THUMBNAIL_SIZE,

                    THUMBNAIL_SIZE

                )

            )

            thumb_path = image_path.replace(

                ".jpg",

                "_thumb.jpg"

            )

            cv2.imwrite(

                thumb_path,

                thumb

            )

            return thumb_path

        except Exception as e:

            print(

                "Thumbnail Error:",

                e

            )

            return None
    # ==========================================================
    # Save Zoom Image
    # ==========================================================

    def save_zoom_image(

        self,

        image_path

    ):

        try:

            if self.zoom <= 1.0:

                return image_path

            image = cv2.imread(

                image_path

            )

            if image is None:

                return None

            height, width = image.shape[:2]

            crop_width = int(

                width / self.zoom

            )

            crop_height = int(

                height / self.zoom

            )

            x = (

                width - crop_width

            ) // 2

            y = (

                height - crop_height

            ) // 2

            crop = image[

                y:y + crop_height,

                x:x + crop_width

            ]

            crop = cv2.resize(

                crop,

                (

                    width,

                    height

                ),

                interpolation=cv2.INTER_CUBIC

            )

            zoom_path = image_path.replace(

                ".jpg",

                "_zoom.jpg"

            )

            cv2.imwrite(

                zoom_path,

                crop

            )

            return zoom_path

        except Exception as e:

            print(

                "Zoom Image Error:",

                e

            )

            return None

    # ==========================================================
    # Save Metadata
    # ==========================================================

    def save_metadata(

        self,

        image_path

    ):

        try:

            metadata = {

                "time": time.strftime(

                    "%Y-%m-%d %H:%M:%S"

                ),

                "camera": "Arducam OV64A40",

                "width": CAPTURE_WIDTH,

                "height": CAPTURE_HEIGHT,

                "zoom": self.zoom,

                "focus": self.focus

            }

            metadata_path = image_path.replace(

                ".jpg",

                ".json"

            )

            with open(

                metadata_path,

                "w"

            ) as file:

                json.dump(

                    metadata,

                    file,

                    indent=4

                )

            return metadata_path

        except Exception as e:

            print(

                "Metadata Error:",

                e

            )

            return None

    # ==========================================================
    # Complete Capture
    # ==========================================================

    def capture_complete(

        self

    ):

        image = self.capture_photo()

        if image is None:

            return None

        thumbnail = self.create_thumbnail(

            image

        )

        zoom = self.save_zoom_image(

            image

        )

        metadata = self.save_metadata(

            image

        )

        return {

            "image": image,

            "thumbnail": thumbnail,

            "zoom": zoom,

            "metadata": metadata

        }
    # ==========================================================
    # Video Filename
    # ==========================================================

    def create_video_name(

        self

    ):

        return time.strftime(

            "%Y%m%d_%H%M%S"

        )

    # ==========================================================
    # Video Directory
    # ==========================================================

    def create_video_directory(

        self

    ):

        Path(

            VIDEO_DIR

        ).mkdir(

            parents=True,

            exist_ok=True

        )

    # ==========================================================
    # Start Recording
    # ==========================================================

    def start_recording(

        self

    ):

        if self.recording:

            return self.video_path

        try:

            self.create_video_directory()

            self.video_path = os.path.join(

                VIDEO_DIR,

                self.create_video_name()

                + ".mp4"

            )

            self.encoder = H264Encoder(

                VIDEO_BITRATE

            )

            self.output = FileOutput(

                self.video_path

            )

            self.picam2.start_encoder(

                self.encoder,

                self.output

            )

            self.recording = True

            return self.video_path

        except Exception as e:

            print(

                "Video Start Error:",

                e

            )

            self.recording = False

            return None

    # ==========================================================
    # Stop Recording
    # ==========================================================

    def stop_recording(

        self

    ):

        if not self.recording:

            return None

        try:

            self.picam2.stop_encoder()

        except Exception as e:

            print(

                "Video Stop Error:",

                e

            )

        self.recording = False

        return self.video_path

    # ==========================================================
    # Recording Status
    # ==========================================================

    def is_recording(

        self

    ):

        return self.recording

    # ==========================================================
    # Current Video
    # ==========================================================

    def current_video(

        self

    ):

        return self.video_path
    # ==========================================================
    # Restart Camera
    # ==========================================================

    def restart(

        self

    ):

        try:

            self.stop()

            time.sleep(

                1

            )

            self.start()

            return True

        except Exception as e:

            print(

                "Restart Error:",

                e

            )

            return False

    # ==========================================================
    # Camera Available
    # ==========================================================

    def is_available(

        self

    ):

        try:

            self.picam2.capture_metadata()

            return True

        except:

            return False

    # ==========================================================
    # Camera Name
    # ==========================================================

    def camera_name(

        self

    ):

        try:

            return self.picam2.camera_properties.get(

                "Model",

                "Unknown Camera"

            )

        except:

            return "Unknown Camera"

    # ==========================================================
    # Close Camera
    # ==========================================================

    def close(

        self

    ):

        try:

            if self.recording:

                self.stop_recording()

        except:

            pass

        try:

            if self.running:

                self.stop()

        except:

            pass

    # ==========================================================
    # Destructor
    # ==========================================================

    def __del__(

        self

    ):

        self.close()


# ==============================================================
# Test
# ==============================================================

if __name__ == "__main__":

    camera = Camera()

    camera.start()

    print(

        "Camera Started"

    )

    print(

        "Camera :",

        camera.camera_name()

    )

    print(

        "Sensor :",

        camera.get_sensor_size()

    )

    while True:

        frame = camera.get_frame()

        cv2.imshow(

            "Micro-Cam Preview",

            frame

        )

        key = cv2.waitKey(

            1

        ) & 0xFF

        if key == ord(

            "c"

        ):

            filename = camera.capture_photo()

            print(

                "Captured:",

                filename

            )

        elif key == ord(

            "v"

        ):

            if camera.is_recording():

                camera.stop_recording()

                print(

                    "Recording Stopped"

                )

            else:

                camera.start_recording()

                print(

                    "Recording Started"

                )

        elif key == ord(

            "q"

        ):

            break

    camera.close()

    cv2.destroyAllWindows()