from flask import (
    Flask,
    render_template,
    Response,
    send_from_directory,
    redirect,
    url_for,
    request,
    jsonify,
)
from camera.camera_controller import CameraController
from camera.streamer import generate_stream
from bt_listener import BTListener
from servo.servo_controller import ServoController

import os
import threading
import time

app = Flask(__name__)

camera = None
servo = None

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)


def get_camera():
    global camera

    if camera is None:
        camera = CameraController()

    return camera


def get_servo_controller():
    global servo

    if servo is None:
        servo = ServoController()

    return servo


def handle_bt_line(line):

    command = line.strip().lower()

    print(f"BT Command: {command}")

    if command == "photo":

        camera = get_camera()

        # wait until first frame is ready
        while camera.get_frame() is None:
            time.sleep(0.1)

        filename = camera.capture_image(IMAGE_DIR)

        print("Captured image")

    elif command == "servo_test":

        print("Future servo functionality goes here")


bt_listener = BTListener(on_msg=handle_bt_line)


def start_bt_listener():

    bt_listener.connect()

    thread = threading.Thread(
        target=bt_listener.listen_forever,
        daemon=True,
    )

    thread.start()

    print("Bluetooth listener started")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/stream")
def stream_page():
    return render_template("stream.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_stream(get_camera()),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/images")
def images_page():

    images = sorted(os.listdir(IMAGE_DIR), reverse=True)

    return render_template("images.html", images=images)


@app.route("/capture")
def capture():

    filename = get_camera().capture_image(IMAGE_DIR)

    return redirect(url_for("images_page"))


@app.route("/image/<filename>")
def view_image(filename):

    return render_template("view_image.html", filename=filename)


@app.route("/images/<filename>")
def serve_image(filename):

    return send_from_directory(IMAGE_DIR, filename)


@app.route("/move_servo", methods=["POST"])
def move_servo():

    data = request.json

    pan = int(data.get("pan", 90))
    tilt = int(data.get("tilt", 90))

    get_servo_controller().move_pan(pan)
    get_servo_controller().move_tilt(tilt)

    return jsonify({"status": "success"})


if __name__ == "__main__":

    start_bt_listener()
    get_camera()
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
