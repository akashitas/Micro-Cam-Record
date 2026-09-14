"""
==========================================================
Micro-Cam
Utility Functions
==========================================================
"""

import os
import json
import shutil
import cv2
import time

from pathlib import Path

from config import *
from datetime import datetime
EVENT_COUNTER = 0
CURRENT_DATE = ""
CURRENT_EVENT_FOLDER = None

# ==========================================================
# Create Folder
# ==========================================================

def create_folder(

    folder

):

    Path(

        folder

    ).mkdir(

        parents=True,

        exist_ok=True

    )


# ==========================================================
# Create All Project Folders
# ==========================================================

def create_project_folders():

    folders = [

        CAPTURE_DIR,

        VIDEO_DIR,

        THUMBNAIL_DIR,

        TEMP_DIR,

        LOG_DIR,

        SETTINGS_DIR

    ]

    for folder in folders:

        create_folder(

            folder

        )


# ==========================================================
# Timestamp
# ==========================================================

def timestamp():

    return time.strftime(

        "%Y%m%d_%H%M%S"

    )

def create_event_folder():

    global EVENT_COUNTER

    global CURRENT_DATE

    global CURRENT_EVENT_FOLDER

    if CURRENT_EVENT_FOLDER is not None:

        return CURRENT_EVENT_FOLDER

    today = datetime.now().strftime(

        "%Y-%m-%d"

    )

    if CURRENT_DATE != today:

        CURRENT_DATE = today

        EVENT_COUNTER = 0

    EVENT_COUNTER += 1

    event_time = datetime.now().strftime(

        "%H-%M-%S"

    )

    event_name = (

        f"Event_{EVENT_COUNTER:03d}_{event_time}"

    )

    CURRENT_EVENT_FOLDER = os.path.join(

        CAPTURE_DIR,

        today,

        event_name

    )

    create_folder(

        CURRENT_EVENT_FOLDER

    )

    return CURRENT_EVENT_FOLDER
# ==========================================================
# Finish Event
# ==========================================================

def finish_event():

    global CURRENT_EVENT_FOLDER

    CURRENT_EVENT_FOLDER = None
# ==========================================================
# Image Filename
# ==========================================================

def image_filename():

    if CURRENT_EVENT_FOLDER is None:
        create_event_folder()

    return os.path.join(
        CURRENT_EVENT_FOLDER,
        "image.jpg"
    )
def video_filename():

    if CURRENT_EVENT_FOLDER is None:
        create_event_folder()

    return os.path.join(
        CURRENT_EVENT_FOLDER,
        "recording.mp4"
    )

# ==========================================================
# Thumbnail Filename
# ==========================================================

def thumbnail_filename(image_path):

    return os.path.join(
        os.path.dirname(image_path),
        "thumbnail.jpg"
    )


# ==========================================================
# Metadata Filename
# ==========================================================

def metadata_filename(image_path):

    return os.path.join(
        os.path.dirname(image_path),
        "metadata.json"
    )

# ==========================================================
# Save Image
# ==========================================================

def save_image(

    image,

    filename=None

):

    if filename is None:

        filename = image_filename()

    cv2.imwrite(

        filename,

        image

    )

    return filename


# ==========================================================
# Save Thumbnail
# ==========================================================

def save_thumbnail(

    image,

    image_path

):

    thumb = cv2.resize(

        image,

        (

            THUMBNAIL_SIZE,

            THUMBNAIL_SIZE

        )

    )

    thumb_path = thumbnail_filename(

        image_path

    )

    cv2.imwrite(

        thumb_path,

        thumb

    )

    return thumb_path
# ==========================================================
# Save Metadata
# ==========================================================

def save_metadata(

    image_path,

    metadata

):

    filename = metadata_filename(

        image_path

    )

    with open(

        filename,

        "w"

    ) as file:

        json.dump(

            metadata,

            file,

            indent=4

        )

    return filename


# ==========================================================
# Load Metadata
# ==========================================================

def load_metadata(

    image_path

):

    filename = metadata_filename(

        image_path

    )

    if not os.path.exists(

        filename

    ):

        return {}

    with open(

        filename,

        "r"

    ) as file:

        return json.load(

            file

        )


# ==========================================================
# Delete File
# ==========================================================

def delete_file(

    filename

):

    try:

        if os.path.exists(

            filename

        ):

            os.remove(

                filename

            )

            return True

    except:

        pass

    return False


# ==========================================================
# Delete Folder
# ==========================================================

def delete_folder(

    folder

):

    try:

        if os.path.exists(

            folder

        ):

            shutil.rmtree(

                folder

            )

            return True

    except:

        pass

    return False


# ==========================================================
# Folder Size
# ==========================================================

def folder_size(

    folder

):

    total = 0

    for root, dirs, files in os.walk(

        folder

    ):

        for file in files:

            filename = os.path.join(

                root,

                file

            )

            if os.path.isfile(

                filename

            ):

                total += os.path.getsize(

                    filename

                )

    return total


# ==========================================================
# Free Disk Space
# ==========================================================

def free_disk_space(

    folder="/"

):

    usage = shutil.disk_usage(

        folder

    )

    return {

        "total": usage.total,

        "used": usage.used,

        "free": usage.free

    }


# ==========================================================
# Format Size
# ==========================================================

def format_size(

    size

):

    for unit in [

        "B",

        "KB",

        "MB",

        "GB",

        "TB"

    ]:

        if size < 1024:

            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


# ==========================================================
# Storage Information
# ==========================================================

def storage_information():

    info = free_disk_space()

    return {

        "Total": format_size(

            info["total"]

        ),

        "Used": format_size(

            info["used"]

        ),

        "Free": format_size(

            info["free"]

        )

    }
# ==========================================================
# Write Log
# ==========================================================

def write_log(

    message

):

    if not ENABLE_LOG:

        return

    create_folder(

        LOG_DIR

    )

    logfile = Path(

        LOG_FILE

    )

    with open(

        logfile,

        "a"

    ) as file:

        file.write(

            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n"

        )


# ==========================================================
# Latest Image
# ==========================================================

def latest_image():

    files = sorted(

        Path(

            CAPTURE_DIR

        ).glob(

            "*.jpg"

        ),

        key=lambda x: x.stat().st_mtime,

        reverse=True

    )

    if len(

        files

    ) == 0:

        return None

    return str(

        files[0]

    )


# ==========================================================
# Latest Video
# ==========================================================

def latest_video():

    files = sorted(

        Path(

            VIDEO_DIR

        ).glob(

            "*.mp4"

        ),

        key=lambda x: x.stat().st_mtime,

        reverse=True

    )

    if len(

        files

    ) == 0:

        return None

    return str(

        files[0]

    )


# ==========================================================
# Clear Temporary Folder
# ==========================================================

def clear_temp():

    if not os.path.exists(

        TEMP_DIR

    ):

        return

    for file in Path(

        TEMP_DIR

    ).glob(

        "*"

    ):

        try:

            if file.is_file():

                file.unlink()

            elif file.is_dir():

                shutil.rmtree(

                    file

                )

        except Exception:

            pass


# ==========================================================
# Count Images
# ==========================================================

def image_count():

    return len(

        list(

            Path(

                CAPTURE_DIR

            ).glob(

                "*.jpg"

            )

        )

    )


# ==========================================================
# Count Videos
# ==========================================================

def video_count():

    return len(

        list(

            Path(

                VIDEO_DIR

            ).glob(

                "*.mp4"

            )

        )

    )


# ==========================================================
# Startup
# ==========================================================

def startup():

    create_project_folders()

    clear_temp()

    write_log(

        "Micro-Cam Started"

    )


# ==========================================================
# Shutdown
# ==========================================================

def shutdown():

    write_log(

        "Micro-Cam Closed"

    )


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    startup()

    print(

        storage_information()

    )

    print(

        "Images :",

        image_count()

    )

    print(

        "Videos :",

        video_count()

    )

    shutdown()
