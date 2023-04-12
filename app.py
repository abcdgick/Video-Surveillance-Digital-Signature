#!/usr/bin/env python
from importlib import import_module
import os
import hashlib
import rsa
from flask import Flask, render_template, Response

if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera


app = Flask(__name__)

(pubkey, privkey) = rsa.newkeys(512)
blake2 = hashlib.blake2s()

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        blake2.update(frame)
        frame_hash = blake2.digest()
        signature = rsa.sign(frame_hash, privkey, 'SHA-256')
        
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)