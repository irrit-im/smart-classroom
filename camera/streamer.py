import time

def generate_stream(camera):

    while True:

        frame = camera.get_jpeg()

        if frame is None:
            time.sleep(0.01)
            continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame +
               b'\r\n')