"""
==========================================================
Micro-Cam
Gallery
==========================================================
"""

import os

from pathlib import Path

from PyQt6.QtCore import *

from PyQt6.QtGui import *

from PyQt6.QtWidgets import *

from config import *


class Gallery(

    QWidget

):

       # Constructor

    def __init__(

        self

    ):

        super().__init__()

        self.build_window()

        self.build_layout()

        self.build_toolbar()

        self.build_gallery()

        self.refresh()

    # Window

    def build_window(

        self

    ):

        self.setWindowTitle(

            "Gallery"

        )

        self.resize(

            1200,

            800

        )

    # Layout

    def build_layout(

        self

    ):

        self.mainLayout = QVBoxLayout()

        self.setLayout(

            self.mainLayout

        )

    # Toolbar

    def build_toolbar(

        self

    ):

        self.toolbar = QHBoxLayout()

        self.refreshButton = QPushButton(

            "🔄 Refresh"

        )

        self.openButton = QPushButton(

            "📷 Open"

        )

        self.deleteButton = QPushButton(

            "🗑 Delete"

        )

        self.closeButton = QPushButton(

            "❌ Close"

        )

        self.toolbar.addWidget(

            self.refreshButton

        )

        self.toolbar.addWidget(

            self.openButton

        )

        self.toolbar.addWidget(

            self.deleteButton

        )

        self.toolbar.addStretch()

        self.toolbar.addWidget(

            self.closeButton

        )

        self.mainLayout.addLayout(

            self.toolbar

        )

    # Gallery Widget

    def build_gallery(

        self

    ):

        self.listWidget = QListWidget()

        self.listWidget.setViewMode(

            QListView.ViewMode.IconMode

        )

        self.listWidget.setIconSize(

            QSize(

                180,

                180

            )

        )

        self.listWidget.setResizeMode(

            QListWidget.ResizeMode.Adjust

        )

        self.listWidget.setSpacing(

            10

        )

        self.mainLayout.addWidget(

            self.listWidget

        )

        self.refreshButton.clicked.connect(

            self.refresh

        )

        self.openButton.clicked.connect(

            self.open_selected

        )

        self.deleteButton.clicked.connect(

            self.delete_selected

        )

        self.closeButton.clicked.connect(

            self.close

        )
    # Refresh Gallery

    def refresh(

        self

    ):

        self.listWidget.clear()

        self.load_images()

        self.load_videos()

    # Load Images

    def load_images(

        self

    ):

        image_dir = Path(

            CAPTURE_DIR

        )

        if not image_dir.exists():

            return

        extensions = [

            ".jpg",

            ".jpeg",

            ".png",

            ".bmp"

        ]

        files = sorted(
            image_dir.rglob("*"),
            reverse=True
            )

        for file in files:

            if file.suffix.lower() not in extensions:

                continue

            item = QListWidgetItem()

            icon = QIcon(

                str(

                    file

                )

            )

            item.setIcon(

                icon

            )

            item.setText(

                file.name

            )

            item.setData(

                Qt.ItemDataRole.UserRole,

                str(

                    file

                )

            )

            self.listWidget.addItem(

                item

            )

    # Load Videos

    def load_videos(

        self

    ):

        video_dir = Path(

            VIDEO_DIR

        )

        if not video_dir.exists():

            return

        files = sorted(
            video_dir.rglob("*.mp4"),
            reverse=True
        )

        for file in files:

            if file.suffix.lower() != ".mp4":

                continue

            item = QListWidgetItem()

            item.setIcon(

                self.style().standardIcon(

                    QStyle.StandardPixmap.SP_MediaPlay

                )

            )

            item.setText(

                file.name

            )

            item.setData(

                Qt.ItemDataRole.UserRole,

                str(

                    file

                )

            )

            self.listWidget.addItem(

                item

            )

    # Selected File

    def selected_file(

        self

    ):

        item = self.listWidget.currentItem()

        if item is None:

            return None

        return item.data(

            Qt.ItemDataRole.UserRole

        )

    # Double Click

    def showEvent(

        self,

        event

    ):

        super().showEvent(

            event

        )

        try:

            self.listWidget.itemDoubleClicked.disconnect()

        except:

            pass

        self.listWidget.itemDoubleClicked.connect(

            self.open_selected

        )
    # Open Selected

    def open_selected(

        self

    ):

        path = self.selected_file()

        if path is None:

            return

        suffix = Path(

            path

        ).suffix.lower()

        if suffix == ".mp4":

            QDesktopServices.openUrl(

                QUrl.fromLocalFile(

                    path

                )

            )

            return

        dialog = QDialog(

            self

        )

        dialog.setWindowTitle(

            Path(

                path

            ).name

        )

        dialog.resize(

            1200,

            900

        )

        layout = QVBoxLayout()

        dialog.setLayout(

            layout

        )

        label = QLabel()

        label.setAlignment(

            Qt.AlignmentFlag.AlignCenter

        )

        pixmap = QPixmap(

            path

        )

        pixmap = pixmap.scaled(

            1100,

            800,

            Qt.AspectRatioMode.KeepAspectRatio,

            Qt.TransformationMode.SmoothTransformation

        )

        label.setPixmap(

            pixmap

        )

        layout.addWidget(

            label

        )

        dialog.exec()

    # Delete Selected

    def delete_selected(

        self

    ):

        path = self.selected_file()

        if path is None:

            return

        reply = QMessageBox.question(

            self,

            "Delete",

            "Delete selected file?",

            QMessageBox.StandardButton.Yes |

            QMessageBox.StandardButton.No

        )

        if reply != QMessageBox.StandardButton.Yes:

            return

        try:

            os.remove(

                path

            )

        except Exception as e:

            QMessageBox.warning(

                self,

                "Error",

                str(

                    e

                )

            )

        self.refresh()

    # ==========================================================
    # Key Press
    # ==========================================================

    def keyPressEvent(

        self,

        event

    ):

        if event.key() == Qt.Key.Key_Delete:

            self.delete_selected()

        elif event.key() == Qt.Key.Key_Return:

            self.open_selected()

        elif event.key() == Qt.Key.Key_Enter:

            self.open_selected()

        elif event.key() == Qt.Key.Key_Escape:

            self.close()

    # Close Event

    def closeEvent(

        self,

        event

    ):

        event.accept()