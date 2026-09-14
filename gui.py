"""
==========================================================
Microscope Camera
GUI
==========================================================
"""

import sys

from PyQt6.QtCore import *

from PyQt6.QtGui import *

from PyQt6.QtWidgets import *

from camera import Camera

from uploader import DriveUploader

from config import *


class CameraWindow(

    QMainWindow

):

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(

        self

    ):

        super().__init__()

        self.camera = Camera()

        self.uploader = DriveUploader()

        self.current_photo = None

        self.recording = False

        self.build_ui()

        self.camera.start()

        self.timer = QTimer()

        self.timer.timeout.connect(

            self.update_preview

        )

        self.timer.start(

            30

        )

    # ==========================================================
    # Build User Interface
    # ==========================================================

    def build_ui(

        self

    ):

        self.setWindowTitle(

            WINDOW_TITLE

        )

        self.resize(

            WINDOW_WIDTH,

            WINDOW_HEIGHT

        )

        self.centralWidget = QWidget()

        self.setCentralWidget(

            self.centralWidget

        )

        self.mainLayout = QVBoxLayout()

        self.mainLayout.setContentsMargins(

            10,

            10,

            10,

            10

        )

        self.mainLayout.setSpacing(

            10

        )

        self.centralWidget.setLayout(

            self.mainLayout

        )

        self.build_header()

        self.build_preview()

        self.build_controls()

        self.build_buttons()

        self.build_status()

        self.connect_signals()

    # ==========================================================
    # Header
    # ==========================================================

    def build_header(

        self

    ):

        layout = QHBoxLayout()

        self.titleLabel = QLabel(

            "Microscope Camera"

        )

        self.titleLabel.setStyleSheet(

            """

            QLabel{

                font-size:24px;

                font-weight:bold;

            }

            """

        )

        self.cameraInfo = QLabel(

            "64 MP"

        )

        self.cameraInfo.setAlignment(

            Qt.AlignmentFlag.AlignRight

        )

        layout.addWidget(

            self.titleLabel

        )

        layout.addStretch()

        layout.addWidget(

            self.cameraInfo

        )

        self.mainLayout.addLayout(

            layout

        )

    # ==========================================================
    # Preview
    # ==========================================================

    def build_preview(

        self

    ):

        self.previewLabel = QLabel()

        self.previewLabel.setMinimumSize(

            1200,

            700

        )

        self.previewLabel.setAlignment(

            Qt.AlignmentFlag.AlignCenter

        )

        self.previewLabel.setStyleSheet(

            """

            QLabel{

                background:#000000;

                border:2px solid #555555;

                border-radius:10px;

            }

            """

        )

        self.mainLayout.addWidget(

            self.previewLabel

        )
    # ==========================================================
    # Camera Controls
    # ==========================================================

    def build_controls(

        self

    ):

        self.controlFrame = QFrame()

        self.controlFrame.setFrameShape(

            QFrame.Shape.StyledPanel

        )

        self.controlLayout = QGridLayout()

        self.controlLayout.setContentsMargins(

            15,

            15,

            15,

            15

        )

        self.controlLayout.setHorizontalSpacing(

            20

        )

        self.controlLayout.setVerticalSpacing(

            15

        )

        self.controlFrame.setLayout(

            self.controlLayout

        )

        # ======================================================
        # Zoom
        # ======================================================

        zoomLabel = QLabel(

            "Zoom"

        )

        self.zoomSlider = QSlider(

            Qt.Orientation.Horizontal

        )

        self.zoomSlider.setRange(

            10,

            100

        )

        self.zoomSlider.setValue(

            10

        )

        self.zoomValue = QLabel(

            "1.0x"

        )

        self.controlLayout.addWidget(

            zoomLabel,

            0,

            0

        )

        self.controlLayout.addWidget(

            self.zoomSlider,

            0,

            1

        )

        self.controlLayout.addWidget(

            self.zoomValue,

            0,

            2

        )

        # ======================================================
        # Focus
        # ======================================================

        focusLabel = QLabel(

            "Focus"

        )

        self.focusSlider = QSlider(

            Qt.Orientation.Horizontal

        )

        self.focusSlider.setRange(

            0,

            100

        )

        self.focusSlider.setValue(

            50

        )

        self.focusValue = QLabel(

            "5.0"

        )

        self.controlLayout.addWidget(

            focusLabel,

            1,

            0

        )

        self.controlLayout.addWidget(

            self.focusSlider,

            1,

            1

        )

        self.controlLayout.addWidget(

            self.focusValue,

            1,

            2

        )

        # ======================================================
        # Exposure
        # ======================================================

        exposureLabel = QLabel(

            "Exposure"

        )

        self.exposureSlider = QSlider(

            Qt.Orientation.Horizontal

        )

        self.exposureSlider.setRange(

            -100,

            100

        )

        self.exposureSlider.setValue(

            0

        )

        self.exposureValue = QLabel(

            "0"

        )

        self.controlLayout.addWidget(

            exposureLabel,

            2,

            0

        )

        self.controlLayout.addWidget(

            self.exposureSlider,

            2,

            1

        )

        self.controlLayout.addWidget(

            self.exposureValue,

            2,

            2

        )

        # ======================================================
        # Brightness
        # ======================================================

        brightnessLabel = QLabel(

            "Brightness"

        )

        self.brightnessSlider = QSlider(

            Qt.Orientation.Horizontal

        )

        self.brightnessSlider.setRange(

            -100,

            100

        )

        self.brightnessSlider.setValue(

            0

        )

        self.brightnessValue = QLabel(

            "0"

        )

        self.controlLayout.addWidget(

            brightnessLabel,

            3,

            0

        )

        self.controlLayout.addWidget(

            self.brightnessSlider,

            3,

            1

        )

        self.controlLayout.addWidget(

            self.brightnessValue,

            3,

            2

        )

        # ======================================================
        # Contrast
        # ======================================================

        contrastLabel = QLabel(

            "Contrast"

        )

        self.contrastSlider = QSlider(

            Qt.Orientation.Horizontal

        )

        self.contrastSlider.setRange(

            0,

            200

        )

        self.contrastSlider.setValue(

            100

        )

        self.contrastValue = QLabel(

            "1.0"

        )

        self.controlLayout.addWidget(

            contrastLabel,

            4,

            0

        )

        self.controlLayout.addWidget(

            self.contrastSlider,

            4,

            1

        )

        self.controlLayout.addWidget(

            self.contrastValue,

            4,

            2

        )

        # ======================================================
        # Sharpness
        # ======================================================

        sharpnessLabel = QLabel(

            "Sharpness"

        )

        self.sharpnessSlider = QSlider(

            Qt.Orientation.Horizontal

        )

        self.sharpnessSlider.setRange(

            0,

            200

        )

        self.sharpnessSlider.setValue(

            100

        )

        self.sharpnessValue = QLabel(

            "1.0"

        )

        self.controlLayout.addWidget(

            sharpnessLabel,

            5,

            0

        )

        self.controlLayout.addWidget(

            self.sharpnessSlider,

            5,

            1

        )

        self.controlLayout.addWidget(

            self.sharpnessValue,

            5,

            2

        )

        # ======================================================
        # White Balance
        # ======================================================

        wbLabel = QLabel(

            "White Balance"

        )

        self.whiteBalance = QComboBox()

        self.whiteBalance.addItems(

            [

                "Auto",

                "Daylight",

                "Cloudy",

                "Tungsten",

                "Fluorescent"

            ]

        )

        self.controlLayout.addWidget(

            wbLabel,

            6,

            0

        )

        self.controlLayout.addWidget(

            self.whiteBalance,

            6,

            1

        )

        self.mainLayout.addWidget(

            self.controlFrame

        )
    # ==========================================================
    # Bottom Camera Buttons
    # ==========================================================

    def build_buttons(

        self

    ):

        self.buttonFrame = QFrame()

        self.buttonLayout = QHBoxLayout()

        self.buttonFrame.setLayout(

            self.buttonLayout

        )

        self.buttonLayout.setContentsMargins(

            10,

            10,

            10,

            10

        )

        self.buttonLayout.setSpacing(

            25

        )

        # ======================================================
        # Gallery Button
        # ======================================================

        self.galleryButton = QPushButton(

            "🖼"

        )

        self.galleryButton.setFixedSize(

            70,

            70

        )

        self.galleryButton.setToolTip(

            "Gallery"

        )

        # ======================================================
        # Video Button
        # ======================================================

        self.videoButton = QPushButton(

            "🎥"

        )

        self.videoButton.setFixedSize(

            70,

            70

        )

        self.videoButton.setToolTip(

            "Video"

        )

        # ======================================================
        # Capture Button
        # ======================================================

        self.captureButton = QPushButton()

        self.captureButton.setFixedSize(

            95,

            95

        )

        self.captureButton.setStyleSheet(

            """

            QPushButton{

                background:white;

                border-radius:47px;

                border:6px solid #777777;

            }

            QPushButton:hover{

                background:#eeeeee;

            }

            QPushButton:pressed{

                background:#cccccc;

            }

            """

        )

        self.captureButton.setToolTip(

            "Capture"

        )

        # ======================================================
        # Upload Button
        # ======================================================

        self.uploadButton = QPushButton(

            "☁"

        )

        self.uploadButton.setFixedSize(

            70,

            70

        )

        self.uploadButton.setToolTip(

            "Upload"

        )

        # ======================================================
        # Settings Button
        # ======================================================

        self.settingsButton = QPushButton(

            "⚙"

        )

        self.settingsButton.setFixedSize(

            70,

            70

        )

        self.settingsButton.setToolTip(

            "Settings"

        )

        # ======================================================
        # Exit Button
        # ======================================================

        self.exitButton = QPushButton(

            "✖"

        )

        self.exitButton.setFixedSize(

            70,

            70

        )

        self.exitButton.setToolTip(

            "Exit"

        )

        self.buttonLayout.addStretch()

        self.buttonLayout.addWidget(

            self.galleryButton

        )

        self.buttonLayout.addWidget(

            self.videoButton

        )

        self.buttonLayout.addWidget(

            self.captureButton

        )

        self.buttonLayout.addWidget(

            self.uploadButton

        )

        self.buttonLayout.addWidget(

            self.settingsButton

        )

        self.buttonLayout.addWidget(

            self.exitButton

        )

        self.buttonLayout.addStretch()

        self.mainLayout.addWidget(

            self.buttonFrame

        )
    # ==========================================================
    # Status Bar
    # ==========================================================

    def build_status(

        self

    ):

        self.statusLabel = QLabel(

            STATUS_READY

        )

        self.statusLabel.setMinimumHeight(

            35

        )

        self.statusLabel.setAlignment(

            Qt.AlignmentFlag.AlignLeft

        )

        self.statusLabel.setStyleSheet(

            """

            QLabel{

                font-size:16px;

                background:#333333;

                color:white;

                padding:8px;

                border-radius:5px;

            }

            """

        )

        self.mainLayout.addWidget(

            self.statusLabel

        )
    # ==========================================================
    # Connect Signals
    # ==========================================================

    def connect_signals(

        self

    ):

        self.captureButton.clicked.connect(

            self.capture_photo

        )

        self.uploadButton.clicked.connect(

            self.upload_photo

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
    # ==========================================================
    # Update Live Preview
    # ==========================================================

    def update_preview(

        self

    ):

        frame = self.camera.get_frame()

        if frame is None:

            return

        height, width, channel = frame.shape

        image = QImage(

            frame.data,

            width,

            height,

            channel * width,

            QImage.Format.Format_RGB888

        )

        pixmap = QPixmap.fromImage(

            image

        )

        pixmap = pixmap.scaled(

            self.previewLabel.size(),

            Qt.AspectRatioMode.KeepAspectRatio,

            Qt.TransformationMode.SmoothTransformation

        )

        self.previewLabel.setPixmap(

            pixmap

        )
    # ==========================================================
    # Zoom
    # ==========================================================

    def zoom_changed(

        self,

        value

    ):

        zoom = value / 10.0

        self.zoomValue.setText(

            f"{zoom:.1f}x"

        )

        self.camera.set_zoom(

            zoom

        )
    # ==========================================================
    # Focus
    # ==========================================================

    def focus_changed(

        self,

        value

    ):

        lens = value / 10.0

        self.focusValue.setText(

            f"{lens:.1f}"

        )

        self.camera.set_focus(

            lens

        )
    # ==========================================================
    # Capture Photo
    # ==========================================================

    def capture_photo(

        self

    ):

        self.statusLabel.setText(

            STATUS_CAPTURING

        )

        QApplication.processEvents()

        filename = self.camera.capture_photo()

        if filename is None:

            self.statusLabel.setText(

                "Capture Failed"

            )

            return

        self.current_photo = filename

        self.statusLabel.setText(

            STATUS_SAVING

        )

        QApplication.processEvents()

        if ENABLE_UPLOAD:

            self.uploader.upload(

                filename

            )

            self.statusLabel.setText(

                STATUS_UPLOADING

            )

        else:

            self.statusLabel.setText(

                STATUS_DONE

            )
    # ==========================================================
    # Upload Current Photo
    # ==========================================================

    def upload_photo(

        self

    ):

        if self.current_photo is None:

            QMessageBox.information(

                self,

                "Upload",

                "Capture a photo first."

            )

            return

        self.uploader.upload(

            self.current_photo

        )

        self.statusLabel.setText(

            STATUS_UPLOADING

        )
    # ==========================================================
    # Close Window
    # ==========================================================

    def closeEvent(

        self,

        event

    ):

        self.timer.stop()

        self.camera.stop()

        self.uploader.stop()

        event.accept()