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
from servo_controller import ServoController, ControlMode
from lcd_adress_display import lcd_display
import config

import os
import threading
import time

os.makedirs(config.IMAGE_DIR, exist_ok=True)

servo_control_mode = ControlMode.NONE

app = Flask(__name__)

camera = None
servo = None


def get_camera() -> CameraController:
    global camera

    if camera is None:
        camera = CameraController()

    return camera


def get_servo_controller() -> ServoController:
    global servo

    if servo is None:
        servo = ServoController()

    return servo


def handle_photo_command() -> None:
    camera = get_camera()
    # wait until first frame is ready
    while camera.get_frame() is None:
        time.sleep(0.1)

    filename = camera.capture_image(config.IMAGE_DIR)

    print("Captured image")

def handle_servo_command(command: str) -> None:

    global servo_control_mode

    if servo_control_mode != ControlMode.BT:
        return

    try:
        x_raw, y_raw = map(int, command.split(","))
    except (ValueError, IndexError):
        return

    servo = get_servo_controller()

    x_offset = x_raw - config.JOYSTICK_X_CENTER
    y_offset = y_raw - config.JOYSTICK_Y_CENTER

    print(
        f"x={x_raw} ({x_offset:+}), "
        f"y={y_raw} ({y_offset:+})"
    )

    # deadzone
    if abs(x_offset) < DEADZONE:
        x_offset = 0

    if abs(y_offset) < DEADZONE:
        y_offset = 0

    # move only the dominant axis
    if abs(x_offset) > abs(y_offset):

        if x_offset > 0:
            servo.move_pan(servo.pan + config.STEP_SIZE)
        else:
            servo.move_pan(servo.pan - config.STEP_SIZE)

    elif abs(y_offset) > 0:

        if y_offset > 0:
            servo.move_tilt(servo.tilt - config.STEP_SIZE)
        else:
            servo.move_tilt(servo.tilt + config.STEP_SIZE)

    print(
        f"pan={servo.pan}, "
        f"tilt={servo.tilt}"
    )

def handle_bt_line(line) -> None:

    command = line.strip().lower()

    print(f"BT Command: {command}")

    if command == "photo":
        handle_photo_command()

    else:
        handle_servo_command(command)


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

    images = sorted(os.listdir(config.IMAGE_DIR), reverse=True)

    return render_template("images.html", images=images)


@app.route("/capture")
def capture():

    filename = get_camera().capture_image(config.IMAGE_DIR)

    return redirect(url_for("images_page"))


@app.route("/image/<filename>")
def view_image(filename):

    return render_template("view_image.html", filename=filename)


@app.route("/images/<filename>")
def serve_image(filename):

    return send_from_directory(config.IMAGE_DIR, filename)

@app.route("/move_servo", methods=["POST"])
def move_servo():

    global servo_control_mode

    print("move_servo route called")
    print(f"Current mode: {servo_control_mode}")

    if servo_control_mode != ControlMode.WEB:
        return jsonify({"status": "ignored"})

    data = request.json

    pan = int(data.get("pan", 90))
    tilt = int(data.get("tilt", 90))

    print(f"Pan={pan}, Tilt={tilt}")

    get_servo_controller().move_pan(pan)
    get_servo_controller().move_tilt(tilt)

    return jsonify({"status": "success"})

@app.route("/servo_control_mode", methods=["POST"])
def set_servo_control_mode():

    global servo_control_mode

    mode = request.json.get("mode")

    if mode == "none":
        servo_control_mode = ControlMode.NONE

    elif mode == "web":
        servo_control_mode = ControlMode.WEB

    elif mode == "bt":
        servo_control_mode = ControlMode.BT

    else:
        return jsonify({"status": "error"}), 400

    print(f"Mode changed to {servo_control_mode}")

    if servo_control_mode == ControlMode.NONE:
        get_servo_controller().idle_all()

    return jsonify({
        "status": "success",
        "mode": servo_control_mode.value
    })

if __name__ == "__main__":
    start_bt_listener()
    get_camera()
    lcd_display()
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
