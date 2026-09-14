"""
==========================================================
Micro-Cam
Main Application
==========================================================
"""

import sys

from PyQt6.QtWidgets import QApplication

from camera_controller import CameraController

from utils import startup

from utils import shutdown


# Main

def main():

    startup()

    app = QApplication(

        sys.argv

    )

    window = CameraController()

    window.show()

    exit_code = app.exec()

    shutdown()

    sys.exit(

        exit_code

    )



# Run


if __name__ == "__main__":

    main()