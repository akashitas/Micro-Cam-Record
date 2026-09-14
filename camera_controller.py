"""
==========================================================
Micro-Cam
Camera Controller
==========================================================
"""

import cv2

from PyQt6.QtCore import *

from PyQt6.QtWidgets import *

from camera import Camera

from camera_gui import CameraGUI

from uploader import DriveUploader

from gallery import Gallery

from config import *

class CameraController(

    CameraGUI

):

    # Constructor
    
    def __init__(

        self

    ):

        super().__init__()

        self.camera = Camera()

        self.uploader = DriveUploader()

        self.gallery = Gallery()

        self.current_image = None

        self.current_video = None

        self.connect_signals()

        self.start_camera()

    # Start Camera
    
    def start_camera(

        self

    ):

        self.camera.start()

        self.timer = QTimer()

        self.timer.timeout.connect(

            self.update_preview

        )

        self.timer.start(

            30

        )

        self.set_status(

            STATUS_READY

        )

     # Connect Signals
    
    def connect_signals(

        self

    ):

        self.captureButton.clicked.connect(

            self.capture_photo

        )

        self.recordButton.clicked.connect(

            self.start_recording

        )

        self.stopButton.clicked.connect(

            self.stop_recording

        )

        self.galleryButton.clicked.connect(

            self.open_gallery

        )

        self.uploadButton.clicked.connect(

            self.upload_current

        )

        self.settingsButton.clicked.connect(

            self.open_settings

        )

        self.exitButton.clicked.connect(

            self.close

        )

        self.zoomSlider.valueChanged.connect(

            self.zoom_changed

        )

        self.focusSlider.valueChanged.connect(

            self.focus_changed

        )

        self.exposureSlider.valueChanged.connect(

            self.exposure_changed

        )

        self.brightnessSlider.valueChanged.connect(

            self.brightness_changed

        )

        self.contrastSlider.valueChanged.connect(

            self.contrast_changed

        )

        self.autoFocusButton.clicked.connect(

            self.camera.autofocus

        )

        self.resetButton.clicked.connect(

            self.reset_camera
        )
      # Update Preview
    

    def update_preview(

        self

    ):

        frame = self.camera.get_frame()

        if frame is None:

            return

        self.display_frame(

            frame

        )

   # Capture Photo
   
    
    def capture_photo(

        self

    ):

        self.set_status(

            STATUS_CAPTURING

        )

        QApplication.processEvents()

        result = self.camera.capture_complete()

        if result is None:

            self.set_status(

                STATUS_ERROR

            )

            return

        self.current_image = result[

            "image"

        ]

        self.set_status(

            STATUS_DONE

        )
 # Start Recording
 
    def start_recording(

        self

    ):

        video = self.camera.start_recording()

        if video is None:

            return

        self.current_video = video

        self.set_recording(

            True

        )

        self.set_status(

            STATUS_RECORDING

        )

   # Stop Recording
    
    def stop_recording(

        self

    ):

        video = self.camera.stop_recording()

        if video is None:

            return

        self.current_video = video

        self.set_recording(

            False

        )

        self.set_status(

            STATUS_DONE

        )

      # Upload Current Image
    
    # ==========================================================
    # Upload Current
    # ==========================================================

    def upload_current(

        self

    ):

        import utils

        if utils.CURRENT_EVENT_FOLDER is None:

            QMessageBox.information(

                self,

                "Upload",

                "No event available."

            )

            return

        print(

            "Uploading:",

            utils.CURRENT_EVENT_FOLDER

        )

        self.set_status(

            STATUS_UPLOADING

        )

        QApplication.processEvents()

        self.uploader.upload_folder(

            utils.CURRENT_EVENT_FOLDER

        )

        self.set_status(

            STATUS_DONE

        )
 # Open Gallery

    def open_gallery(

        self

    ):

        self.gallery.refresh()

        self.gallery.show()

    # Open Settings

    def open_settings(

        self

    ):

        QMessageBox.information(

            self,

            "Settings",

            "Camera Settings Window Coming Soon."

        )
    # Zoom Changed

    def zoom_changed(

        self,

        value

    ):

        zoom = value / 10.0

        self.camera.set_zoom(

            zoom

        )

        self.set_zoom_label(

            zoom

        )

    # Focus Changed

    def focus_changed(

        self,

        value

    ):

        focus = value / 10.0

        self.camera.set_focus(

            focus

        )

        self.set_focus_label(

            focus

        )

    # Exposure Changed

    def exposure_changed(

        self,

        value

    ):

        self.camera.set_exposure(

            value

        )

   # Brightness Changed

    def brightness_changed(

        self,

        value

    ):

        self.camera.set_brightness(

            value / 100.0

        )

    # Contrast Changed

    def contrast_changed(

        self,

        value

    ):

        self.camera.set_contrast(

            value / 100.0

        )

    # White Balance Changed

    def white_balance_changed(

        self,

        index

    ):

        mode = self.whiteBalance.currentText()

        if mode == "Auto":

            self.camera.enable_auto_white_balance()

        elif mode == "Daylight":

            self.camera.set_white_balance(

                2.0,

                1.6

            )

        elif mode == "Cloudy":

            self.camera.set_white_balance(

                2.2,

                1.5

            )

        elif mode == "Indoor":

            self.camera.set_white_balance(

                1.5,

                2.2

            )

        elif mode == "Fluorescent":

            self.camera.set_white_balance(

                1.4,

                2.4

            )

        elif mode == "Tungsten":

            self.camera.set_white_balance(

                1.2,

                2.8

            )

    # Reset Camera
    
    def reset_camera(

        self

    ):

        self.camera.reset_controls()

        self.zoomSlider.setValue(

            10

        )

        self.focusSlider.setValue(

            50

        )

        self.exposureSlider.setValue(

            0

        )

        self.brightnessSlider.setValue(

            0

        )

        self.contrastSlider.setValue(

            100

        )

        self.whiteBalance.setCurrentIndex(

            0

        )

        self.set_zoom_label(

            1.0

        )

        self.set_focus_label(

            DEFAULT_FOCUS

        )

        self.set_status(

            STATUS_READY

        )

   # Close Event

    def closeEvent(

        self,

        event

    ):

        try:

            self.timer.stop()

        except:

            pass

        try:

            self.camera.close()

        except:

            pass

        event.accept()