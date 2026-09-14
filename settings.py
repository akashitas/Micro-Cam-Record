"""
==========================================================
Micro-Cam
Settings Window
==========================================================
"""

import json

from pathlib import Path

from PyQt6.QtCore import *

from PyQt6.QtWidgets import *

from config import *


class SettingsWindow(

    QDialog

):

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(

        self,

        camera

    ):

        super().__init__()

        self.camera = camera

        self.settings_file = Path(

            SETTINGS_DIR

        ) / "settings.json"

        self.build_window()

        self.build_layout()

        self.load_settings()

    # ==========================================================
    # Window
    # ==========================================================

    def build_window(

        self

    ):

        self.setWindowTitle(

            "Camera Settings"

        )

        self.resize(

            500,

            650

        )

    # ==========================================================
    # Layout
    # ==========================================================

    def build_layout(

        self

    ):

        self.layout = QFormLayout()

        self.setLayout(

            self.layout

        )

        # ======================================================
        # Zoom
        # ======================================================

        self.zoomSpin = QDoubleSpinBox()

        self.zoomSpin.setRange(

            MIN_ZOOM,

            MAX_ZOOM

        )

        self.zoomSpin.setSingleStep(

            0.1

        )

        self.layout.addRow(

            "Default Zoom",

            self.zoomSpin

        )

        # ======================================================
        # Focus
        # ======================================================

        self.focusSpin = QDoubleSpinBox()

        self.focusSpin.setRange(

            MIN_FOCUS,

            MAX_FOCUS

        )

        self.focusSpin.setSingleStep(

            0.1

        )

        self.layout.addRow(

            "Default Focus",

            self.focusSpin

        )

        # ======================================================
        # Exposure
        # ======================================================

        self.exposureSpin = QSpinBox()

        self.exposureSpin.setRange(

            MIN_EXPOSURE,

            MAX_EXPOSURE

        )

        self.layout.addRow(

            "Exposure",

            self.exposureSpin

        )

        # ======================================================
        # Brightness
        # ======================================================

        self.brightnessSpin = QDoubleSpinBox()

        self.brightnessSpin.setRange(

            -1,

            1

        )

        self.brightnessSpin.setSingleStep(

            0.1

        )

        self.layout.addRow(

            "Brightness",

            self.brightnessSpin

        )

        # ======================================================
        # Contrast
        # ======================================================

        self.contrastSpin = QDoubleSpinBox()

        self.contrastSpin.setRange(

            0,

            3

        )

        self.contrastSpin.setSingleStep(

            0.1

        )

        self.layout.addRow(

            "Contrast",

            self.contrastSpin

        )

        # ======================================================
        # Saturation
        # ======================================================

        self.saturationSpin = QDoubleSpinBox()

        self.saturationSpin.setRange(

            0,

            3

        )

        self.saturationSpin.setSingleStep(

            0.1

        )

        self.layout.addRow(

            "Saturation",

            self.saturationSpin

        )

        # ======================================================
        # Sharpness
        # ======================================================

        self.sharpnessSpin = QDoubleSpinBox()

        self.sharpnessSpin.setRange(

            0,

            5

        )

        self.sharpnessSpin.setSingleStep(

            0.1

        )

        self.layout.addRow(

            "Sharpness",

            self.sharpnessSpin

        )

        # ======================================================
        # White Balance
        # ======================================================

        self.whiteBalance = QComboBox()

        self.whiteBalance.addItems(

            WHITE_BALANCE_MODES

        )

        self.layout.addRow(

            "White Balance",

            self.whiteBalance

        )
        # ======================================================
        # Auto Focus
        # ======================================================

        self.autoFocus = QCheckBox(

            "Enable Continuous Autofocus"

        )

        self.layout.addRow(

            self.autoFocus

        )

        # ======================================================
        # Upload
        # ======================================================

        self.uploadCheck = QCheckBox(

            "Upload After Capture"

        )

        self.layout.addRow(

            self.uploadCheck

        )

        # ======================================================
        # Save Metadata
        # ======================================================

        self.metadataCheck = QCheckBox(

            "Save Metadata"

        )

        self.layout.addRow(

            self.metadataCheck

        )

        # ======================================================
        # Save Thumbnail
        # ======================================================

        self.thumbnailCheck = QCheckBox(

            "Save Thumbnail"

        )

        self.layout.addRow(

            self.thumbnailCheck

        )

        # ======================================================
        # Save Zoom Image
        # ======================================================

        self.zoomImageCheck = QCheckBox(

            "Save Zoom Image"

        )

        self.layout.addRow(

            self.zoomImageCheck

        )

        # ======================================================
        # Buttons
        # ======================================================

        self.buttonLayout = QHBoxLayout()

        self.saveButton = QPushButton(

            "💾 Save"

        )

        self.loadButton = QPushButton(

            "📂 Load"

        )

        self.applyButton = QPushButton(

            "✔ Apply"

        )

        self.defaultButton = QPushButton(

            "↺ Defaults"

        )

        self.closeButton = QPushButton(

            "❌ Close"

        )

        self.buttonLayout.addWidget(

            self.saveButton

        )

        self.buttonLayout.addWidget(

            self.loadButton

        )

        self.buttonLayout.addWidget(

            self.applyButton

        )

        self.buttonLayout.addWidget(

            self.defaultButton

        )

        self.buttonLayout.addWidget(

            self.closeButton

        )

        self.layout.addRow(

            self.buttonLayout

        )

        # ======================================================
        # Connections
        # ======================================================

        self.saveButton.clicked.connect(

            self.save_settings

        )

        self.loadButton.clicked.connect(

            self.load_settings

        )

        self.applyButton.clicked.connect(

            self.apply_settings

        )

        self.defaultButton.clicked.connect(

            self.restore_defaults

        )

        self.closeButton.clicked.connect(

            self.accept

        )
    # ==========================================================
    # Save Settings
    # ==========================================================

    def save_settings(

        self

    ):

        data = {

            "zoom":

            self.zoomSpin.value(),

            "focus":

            self.focusSpin.value(),

            "exposure":

            self.exposureSpin.value(),

            "brightness":

            self.brightnessSpin.value(),

            "contrast":

            self.contrastSpin.value(),

            "saturation":

            self.saturationSpin.value(),

            "sharpness":

            self.sharpnessSpin.value(),

            "white_balance":

            self.whiteBalance.currentText(),

            "autofocus":

            self.autoFocus.isChecked(),

            "upload":

            self.uploadCheck.isChecked(),

            "metadata":

            self.metadataCheck.isChecked(),

            "thumbnail":

            self.thumbnailCheck.isChecked(),

            "zoom_image":

            self.zoomImageCheck.isChecked()

        }

        try:

            self.settings_file.parent.mkdir(

                parents=True,

                exist_ok=True

            )

            with open(

                self.settings_file,

                "w"

            ) as file:

                json.dump(

                    data,

                    file,

                    indent=4

                )

            QMessageBox.information(

                self,

                "Settings",

                "Settings saved successfully."

            )

        except Exception as e:

            QMessageBox.warning(

                self,

                "Error",

                str(

                    e

                )

            )

    # ==========================================================
    # Load Settings
    # ==========================================================

    def load_settings(

        self

    ):

        if not self.settings_file.exists():

            self.restore_defaults()

            return

        try:

            with open(

                self.settings_file,

                "r"

            ) as file:

                data = json.load(

                    file

                )

            self.zoomSpin.setValue(

                data.get(

                    "zoom",

                    DEFAULT_ZOOM

                )

            )

            self.focusSpin.setValue(

                data.get(

                    "focus",

                    DEFAULT_FOCUS

                )

            )

            self.exposureSpin.setValue(

                data.get(

                    "exposure",

                    DEFAULT_EXPOSURE

                )

            )

            self.brightnessSpin.setValue(

                data.get(

                    "brightness",

                    DEFAULT_BRIGHTNESS

                )

            )

            self.contrastSpin.setValue(

                data.get(

                    "contrast",

                    DEFAULT_CONTRAST

                )

            )

            self.saturationSpin.setValue(

                data.get(

                    "saturation",

                    DEFAULT_SATURATION

                )

            )

            self.sharpnessSpin.setValue(

                data.get(

                    "sharpness",

                    DEFAULT_SHARPNESS

                )

            )

            mode = data.get(

                "white_balance",

                "Auto"

            )

            index = self.whiteBalance.findText(

                mode

            )

            if index >= 0:

                self.whiteBalance.setCurrentIndex(

                    index

                )

            self.autoFocus.setChecked(

                data.get(

                    "autofocus",

                    True

                )

            )

            self.uploadCheck.setChecked(

                data.get(

                    "upload",

                    ENABLE_UPLOAD

                )

            )

            self.metadataCheck.setChecked(

                data.get(

                    "metadata",

                    SAVE_METADATA

                )

            )

            self.thumbnailCheck.setChecked(

                data.get(

                    "thumbnail",

                    SAVE_THUMBNAIL

                )

            )

            self.zoomImageCheck.setChecked(

                data.get(

                    "zoom_image",

                    SAVE_ZOOM_IMAGE

                )

            )

        except Exception as e:

            QMessageBox.warning(

                self,

                "Error",

                str(

                    e

                )

            )
    # ==========================================================
    # Apply Settings
    # ==========================================================

    def apply_settings(

        self

    ):

        try:

            self.camera.set_zoom(

                self.zoomSpin.value()

            )

            if self.autoFocus.isChecked():

                self.camera.enable_continuous_autofocus()

            else:

                self.camera.set_focus(

                    self.focusSpin.value()

                )

            self.camera.set_exposure(

                self.exposureSpin.value()

            )

            self.camera.set_brightness(

                self.brightnessSpin.value()

            )

            self.camera.set_contrast(

                self.contrastSpin.value()

            )

            self.camera.set_saturation(

                self.saturationSpin.value()

            )

            self.camera.set_sharpness(

                self.sharpnessSpin.value()

            )

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

            QMessageBox.information(

                self,

                "Settings",

                "Settings applied successfully."

            )

        except Exception as e:

            QMessageBox.warning(

                self,

                "Error",

                str(

                    e

                )

            )

    # ==========================================================
    # Restore Defaults
    # ==========================================================

    def restore_defaults(

        self

    ):

        self.zoomSpin.setValue(

            DEFAULT_ZOOM

        )

        self.focusSpin.setValue(

            DEFAULT_FOCUS

        )

        self.exposureSpin.setValue(

            DEFAULT_EXPOSURE

        )

        self.brightnessSpin.setValue(

            DEFAULT_BRIGHTNESS

        )

        self.contrastSpin.setValue(

            DEFAULT_CONTRAST

        )

        self.saturationSpin.setValue(

            DEFAULT_SATURATION

        )

        self.sharpnessSpin.setValue(

            DEFAULT_SHARPNESS

        )

        self.whiteBalance.setCurrentText(

            "Auto"

        )

        self.autoFocus.setChecked(

            True

        )

        self.uploadCheck.setChecked(

            ENABLE_UPLOAD

        )

        self.metadataCheck.setChecked(

            SAVE_METADATA

        )

        self.thumbnailCheck.setChecked(

            SAVE_THUMBNAIL

        )

        self.zoomImageCheck.setChecked(

            SAVE_ZOOM_IMAGE

        )

    # ==========================================================
    # Close Event
    # ==========================================================

    def closeEvent(

        self,

        event

    ):

        event.accept()