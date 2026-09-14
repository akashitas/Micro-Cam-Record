"""
==========================================================
Micro-Cam
Camera GUI
==========================================================
"""

from PyQt6.QtCore import *

from PyQt6.QtGui import *

from PyQt6.QtWidgets import *
import cv2

from config import *


class CameraGUI(

    QMainWindow

):

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(

        self

    ):

        super().__init__()

        self.build_window()

        self.build_layout()

        self.build_preview()

        self.build_right_panel()

        self.build_bottom_toolbar()

        self.build_statusbar()

    # ==========================================================
    # Window
    # ==========================================================

    def build_window(

        self

    ):

        self.setWindowTitle(

            WINDOW_TITLE

        )

        screen = QApplication.primaryScreen()

        geometry = screen.availableGeometry()

        width = geometry.width()

        height = geometry.height()

        if width <= 1024:

            self.resize(

                width,

                height

            )

        else:

            self.resize(

                int(width * 0.90),

                int(height * 0.90)

            )

        self.central = QWidget()

        self.setCentralWidget(

            self.central

        )

    # ==========================================================
    # Main Layout
    # ==========================================================

    def build_layout(

        self

    ):

        self.mainLayout = QVBoxLayout()

        self.central.setLayout(

            self.mainLayout

        )

        self.topLayout = QHBoxLayout()

        self.mainLayout.addLayout(

            self.topLayout

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

                background:black;

                border:2px solid gray;

            }

            """

        )

        self.topLayout.addWidget(

            self.previewLabel,

            5

        )
    # ==========================================================
    # Right Control Panel
    # ==========================================================

    def build_right_panel(

        self

    ):

        self.rightWidget = QWidget()

        self.rightLayout = QVBoxLayout()

        self.rightWidget.setLayout(

            self.rightLayout

        )

        self.rightWidget.setMaximumWidth(

            320

        )

        self.topLayout.addWidget(

            self.rightWidget,

            1

        )

        # ======================================================
        # Zoom
        # ======================================================

        zoomTitle = QLabel(

            "Zoom"

        )

        zoomTitle.setStyleSheet(

            "font-weight:bold;"

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

        self.rightLayout.addWidget(

            zoomTitle

        )

        self.rightLayout.addWidget(

            self.zoomSlider

        )

        self.rightLayout.addWidget(

            self.zoomValue

        )

        # ======================================================
        # Focus
        # ======================================================

        focusTitle = QLabel(

            "Focus"

        )

        focusTitle.setStyleSheet(

            "font-weight:bold;"

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

        self.rightLayout.addWidget(

            focusTitle

        )

        self.rightLayout.addWidget(

            self.focusSlider

        )

        self.rightLayout.addWidget(

            self.focusValue

        )

        # ======================================================
        # Exposure
        # ======================================================

        exposureTitle = QLabel(

            "Exposure"

        )

        exposureTitle.setStyleSheet(

            "font-weight:bold;"

        )

        self.exposureSlider = QSlider(

            Qt.Orientation.Horizontal

        )

        self.exposureSlider.setRange(

            -8,

            8

        )

        self.exposureSlider.setValue(

            0

        )

        self.rightLayout.addWidget(

            exposureTitle

        )

        self.rightLayout.addWidget(

            self.exposureSlider

        )

        # ======================================================
        # Brightness
        # ======================================================

        brightnessTitle = QLabel(

            "Brightness"

        )

        brightnessTitle.setStyleSheet(

            "font-weight:bold;"

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

        self.rightLayout.addWidget(

            brightnessTitle

        )

        self.rightLayout.addWidget(

            self.brightnessSlider

        )

        # ======================================================
        # Contrast
        # ======================================================

        contrastTitle = QLabel(

            "Contrast"

        )

        contrastTitle.setStyleSheet(

            "font-weight:bold;"

        )

        self.contrastSlider = QSlider(

            Qt.Orientation.Horizontal

        )

        self.contrastSlider.setRange(

            0,

            300

        )

        self.contrastSlider.setValue(

            100

        )

        self.rightLayout.addWidget(

            contrastTitle

        )

        self.rightLayout.addWidget(

            self.contrastSlider

        )

        # ======================================================
        # White Balance
        # ======================================================

        wbTitle = QLabel(

            "White Balance"

        )

        wbTitle.setStyleSheet(

            "font-weight:bold;"

        )

        self.whiteBalance = QComboBox()

        self.whiteBalance.addItems(

            WHITE_BALANCE_MODES

        )

        self.rightLayout.addWidget(

            wbTitle

        )

        self.rightLayout.addWidget(

            self.whiteBalance

        )

        # ======================================================
        # Buttons
        # ======================================================

        self.autoFocusButton = QPushButton(

            "Auto Focus"

        )

        self.resetButton = QPushButton(

            "Reset Camera"

        )

        self.rightLayout.addWidget(

            self.autoFocusButton

        )
        self.rightLayout.addWidget(

            self.resetButton

        )

        self.rightLayout.addStretch()

            # ==========================================================
    # Bottom Toolbar
    # ==========================================================

    def build_bottom_toolbar(

        self

    ):

        self.toolbarWidget = QWidget()

        self.toolbarLayout = QHBoxLayout()

        self.toolbarWidget.setLayout(

            self.toolbarLayout

        )

        self.mainLayout.addWidget(

            self.toolbarWidget

        )

        # ======================================================
        # Capture
        # ======================================================

        self.captureButton = QPushButton(

            "📷 Capture"

        )

        self.captureButton.setMinimumHeight(

            BUTTON_HEIGHT

        )

        self.captureButton.setMinimumWidth(

            BUTTON_WIDTH

        )

        self.toolbarLayout.addWidget(

            self.captureButton

        )

        # ======================================================
        # Record
        # ======================================================

        self.recordButton = QPushButton(

            "🎥 Record"

        )

        self.recordButton.setMinimumHeight(

            BUTTON_HEIGHT

        )

        self.recordButton.setMinimumWidth(

            BUTTON_WIDTH

        )

        self.toolbarLayout.addWidget(

            self.recordButton

        )

        # ======================================================
        # Stop
        # ======================================================

        self.stopButton = QPushButton(

            "⏹ Stop"

        )

        self.stopButton.setMinimumHeight(

            BUTTON_HEIGHT

        )

        self.stopButton.setMinimumWidth(

            BUTTON_WIDTH

        )

        self.toolbarLayout.addWidget(

            self.stopButton

        )

        # ======================================================
        # Gallery
        # ======================================================

        self.galleryButton = QPushButton(

            "🖼 Gallery"

        )

        self.galleryButton.setMinimumHeight(

            BUTTON_HEIGHT

        )

        self.galleryButton.setMinimumWidth(

            BUTTON_WIDTH

        )

        self.toolbarLayout.addWidget(

            self.galleryButton

        )

        # ======================================================
        # Upload
        # ======================================================

        self.uploadButton = QPushButton(

            "☁ Upload"

        )

        self.uploadButton.setMinimumHeight(

            BUTTON_HEIGHT

        )

        self.uploadButton.setMinimumWidth(

            BUTTON_WIDTH

        )

        self.toolbarLayout.addWidget(

            self.uploadButton

        )

        # ======================================================
        # Settings
        # ======================================================

        self.settingsButton = QPushButton(

            "⚙ Settings"

        )

        self.settingsButton.setMinimumHeight(

            BUTTON_HEIGHT

        )

        self.settingsButton.setMinimumWidth(

            BUTTON_WIDTH

        )

        self.toolbarLayout.addWidget(

            self.settingsButton

        )

        # ======================================================
        # Exit
        # ======================================================

        self.exitButton = QPushButton(

            "❌ Exit"

        )

        self.exitButton.setMinimumHeight(

            BUTTON_HEIGHT

        )

        self.exitButton.setMinimumWidth(

            BUTTON_WIDTH

        )

        self.toolbarLayout.addWidget(

            self.exitButton
        )

        self.toolbarLayout.addStretch()
    # ==========================================================
    # Status Bar
    # ==========================================================

    def build_statusbar(

        self

    ):

        self.statusWidget = QWidget()

        self.statusLayout = QHBoxLayout()

        self.statusWidget.setLayout(

            self.statusLayout

        )

        self.mainLayout.addWidget(

            self.statusWidget

        )

        self.statusLabel = QLabel(

            STATUS_READY

        )

        self.statusLabel.setMinimumWidth(

            250

        )

        self.zoomLabel = QLabel(

            "Zoom : 1.0x"

        )

        self.focusLabel = QLabel(

            "Focus : AF"

        )

        self.resolutionLabel = QLabel(

            f"{PREVIEW_WIDTH} × {PREVIEW_HEIGHT}"

        )

        self.recordLabel = QLabel(

            "Recording : OFF"

        )

        self.progressBar = QProgressBar()

        self.progressBar.setMaximum(

            100

        )

        self.progressBar.setValue(

            0

        )

        self.progressBar.setVisible(

            False

        )

        self.statusLayout.addWidget(

            self.statusLabel

        )

        self.statusLayout.addStretch()

        self.statusLayout.addWidget(

            self.zoomLabel

        )

        self.statusLayout.addWidget(

            self.focusLabel

        )

        self.statusLayout.addWidget(

            self.resolutionLabel

        )

        self.statusLayout.addWidget(

            self.recordLabel

        )

        self.statusLayout.addWidget(

            self.progressBar

        )

    # ==========================================================
    # Status Text
    # ==========================================================

    def set_status(

        self,

        text

    ):

        self.statusLabel.setText(

            text

        )

    # ==========================================================
    # Update Zoom Label
    # ==========================================================

    def set_zoom_label(

        self,

        zoom

    ):

        self.zoomLabel.setText(

            f"Zoom : {zoom:.1f}x"

        )

    # ==========================================================
    # Update Focus Label
    # ==========================================================

    def set_focus_label(

        self,

        value

    ):

        self.focusLabel.setText(

            f"Focus : {value:.2f}"

        )

    # ==========================================================
    # Recording Status
    # ==========================================================

    def set_recording(

        self,

        state

    ):

        if state:

            self.recordLabel.setText(

                "Recording : ON"

            )

        else:

            self.recordLabel.setText(

                "Recording : OFF"

            )

    # ==========================================================
    # Progress
    # ==========================================================

    def show_progress(

        self,

        value

    ):

        self.progressBar.setVisible(

            True

        )

        self.progressBar.setValue(

            value

        )

    # ==========================================================
    # Hide Progress
    # ==========================================================

    def hide_progress(

        self

    ):

        self.progressBar.setVisible(

            False

        )

    # ==========================================================
    # Display Preview
    # ==========================================================
    # ==========================================================
    # Display Preview
    # ==========================================================

    def display_frame(

        self,

        frame

    ):

        if frame is None:

            return

        frame = cv2.cvtColor(

            frame,

            cv2.COLOR_BGR2RGB

        )

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
    # Close Event
    # ==========================================================

    def closeEvent(

        self,

        event

    ):

        event.accept()