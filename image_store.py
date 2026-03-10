import os
import time
import config

class ImageStore:

    def __init__(self):
        os.makedirs(config.IMAGE_DIR, exist_ok=True)

    def new_image_path(self):

        timestamp = time.strftime("%Y%m%d_%H%M%S")

        return f"{config.IMAGE_DIR}/board_{timestamp}.jpg"

    def list_images(self):

        return sorted(os.listdir(config.IMAGE_DIR))