from flask import Flask, render_template, Response, send_from_directory, redirect, url_for, request, jsonify
from camera.camera_controller import CameraController
from camera.streamer import generate_stream
import os
from servo.servo_controller import ServoController

app = Flask(__name__)

camera = None
servo = None

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

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/stream")
def stream_page():
    return render_template("stream.html")


@app.route("/video_feed")
def video_feed():
    return Response(generate_stream(get_camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


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
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)