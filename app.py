#!/usr/bin/env python
from random import random
import socket
import requests
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import BLAKE2s
from flask import Flask, render_template, Response

from camera_opencv import Camera

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
private_ip = s.getsockname()[0]
public_ip = requests.get('https://api.ipify.org').text
s.close()

app = Flask(__name__)

key = RSA.generate(2048)
public_key = key.publickey().export_key()
private_key = key.export_key()

frame = b''

# with open("public_key.pem", "wb") as file:
#     file.write(public_key)

@app.route('/')
def index():
    return render_template('index.html', public_key=public_key.decode())

def sign_frame():
    global frame
    blake2_hash = BLAKE2s.new()
    blake2_hash.update(frame)

    signature = pss.new(key).sign(blake2_hash)
    
    return signature

def gen(camera):
    global frame
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()

        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/video_text')
def video_text():
    global frame
    signature = sign_frame()
    return Response(frame.hex() + ',' + signature.hex(), mimetype='text/plain')

def check_port():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', 5000))
        return True
    except OSError:
        return False

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', threaded=True)
    except:
        if check_port():
            print(f"Port default (5000) dapat digunakan.\nPeriksa kembali perintah yang anda masukkan.")
        else:
            print(f"Port default (5000) tidak dapat digunakan.\nMohon gunakan port lain seperti port {random.randint(1024, 49151)}")

print(f"Private IP: {private_ip}")
print(f"Public IP: {public_ip}")