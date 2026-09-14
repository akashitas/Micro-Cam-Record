"""
==========================================================
Micro-Cam
Google Drive Uploader
==========================================================
"""

import os

import subprocess

import threading

from PyQt6.QtCore import *

from config import *


class DriveUploader(

    QObject

):

    # Signals

    finished = pyqtSignal(

        bool,

        str

    )

    progress = pyqtSignal(

        str

    )

    # Constructor

    def __init__(

        self

    ):

        super().__init__()

        self.thread = None

        self.running = False

    # Upload

    def upload(

        self,

        filepath

    ):

        if self.running:

            return

        if not os.path.exists(

            filepath

        ):

            self.finished.emit(

                False,

                "File Not Found"

            )

            return

        self.running = True

        self.thread = threading.Thread(

            target=self._upload,

            args=(

                filepath,

            ),

            daemon=True

        )

        self.thread.start()

    # Upload Thread

    def _upload(

        self,

        filepath

    ):

        try:

            self.progress.emit(

                "Uploading..."

            )

            destination = (

                f"{RCLONE_REMOTE}:{RCLONE_FOLDER}"

            )

            command = [

                "rclone",

                "copy",

                filepath,

                destination,

                "--progress"

            ]

            process = subprocess.run(

                command,

                capture_output=True,

                text=True

            )

            if process.returncode == 0:

                self.finished.emit(

                    True,

                    filepath

                )

            else:

                self.finished.emit(

                    False,

                    process.stderr

                )

        except Exception as e:

            self.finished.emit(

                False,

                str(

                    e

                )

            )

        self.running = False
    # Upload Image

    def upload_image(

        self,

        image_path

    ):

        self.upload(

            image_path

        )

    # Upload Video

    def upload_video(

        self,

        video_path

    ):

        self.upload(

            video_path

        )

    # Upload Folder

    def upload_folder(

        self,

        folder

    ):

        if self.running:

            return

        if not os.path.isdir(

            folder

        ):

            self.finished.emit(

                False,

                "Folder Not Found"

            )

            return

        self.running = True

        self.thread = threading.Thread(

            target=self._upload_folder,

            args=(

                folder,

            ),

            daemon=True

        )

        self.thread.start()

    # Folder Upload Thread

    def _upload_folder(

        self,

        folder

    ):

        try:

            self.progress.emit(

                "Uploading Folder..."

            )

            relative_path = os.path.relpath(
                folder,
                CAPTURE_DIR
            )
            destination = (
                f"{RCLONE_REMOTE}:{RCLONE_FOLDER}"
            )

            command = [

                "rclone",

                "copy",

                folder,

                destination,

                "--progress"

            ]

            process = subprocess.run(

                command,

                capture_output=True,

                text=True

            )

            if process.returncode == 0:

                if DELETE_AFTER_UPLOAD:

                    try:

                        for root, dirs, files in os.walk(

                            folder,

                            topdown=False

                        ):

                            for file in files:

                                os.remove(

                                    os.path.join(

                                        root,

                                        file

                                    )

                                )

                            for directory in dirs:

                                os.rmdir(

                                    os.path.join(

                                        root,

                                        directory

                                    )

                                )

                        os.rmdir(

                            folder

                        )

                    except Exception:

                        pass

                self.finished.emit(

                    True,

                    folder

                )

            else:

                self.finished.emit(

                    False,

                    process.stderr

                )

        except Exception as e:

            self.finished.emit(

                False,

                str(

                    e

                )

            )

        self.running = False

    # Cancel Upload

    def cancel(

        self

    ):

        self.running = False

    # Upload Running

    def is_running(

        self

    ):

        return self.running

    # Wait For Thread

    def wait(

        self

    ):

        if self.thread is not None:

            self.thread.join()

    # Stop

    def stop(

        self

    ):

        self.cancel()

        self.wait()