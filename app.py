#!/usr/bin/env python
import socket
import requests
from importlib import import_module
import os
import hashlib
import rsa
from flask import Flask, render_template, Response

from camera_opencv import Camera

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
private_ip = s.getsockname()[0]
print(s.getsockname())
public_ip = requests.get('https://api.ipify.org').text
s.close()

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

print(f"Private IP: {private_ip}")
print(f"Public IP: {public_ip}")