from picamera2 import Picamera2
import cv2
import threading
import time
import os


class CameraController:

    def __init__(self):

        self.picam2 = Picamera2()

        self.picam2.configure(
            self.picam2.create_preview_configuration(
                main={"format": "XRGB8888", "size": (640, 480)}
            )
        )

        self.picam2.start()
        self.picam2.set_controls({"FrameRate": 4})

        time.sleep(2)

        self.frame = None
        self.lock = threading.Lock()

        thread = threading.Thread(target=self.update_frames, daemon=True)
        thread.start()

    def update_frames(self):

        while True:

            frame = self.picam2.capture_array()

            with self.lock:
                self.frame = frame

    def get_frame(self):

        with self.lock:
            if self.frame is None:
                return None

            return self.frame.copy()

    def get_jpeg(self):

        frame = self.get_frame()

        if frame is None:
            return None

        ret, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

        return buffer.tobytes()

    def capture_image(self, folder):

        frame = self.get_frame()

        if frame is None:
            raise RuntimeError("Camera frame not ready")

        timestamp = time.strftime("%Y%m%d_%H%M%S")

        filename = f"board_{timestamp}.jpg"

        path = os.path.join(folder, filename)

        cv2.imwrite(path, frame)

        return filename