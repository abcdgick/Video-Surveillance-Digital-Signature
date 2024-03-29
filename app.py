#!/usr/bin/env python
import random
import sys
import socket
import requests
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import BLAKE2b
from flask import Flask, render_template, Response

from camera_opencv import Camera

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
private_ip = s.getsockname()[0]
public_ip = requests.get('https://api.ipify.org').text
s.close()

if len(sys.argv) >= 10:
    if sys.argv[8] == "True":
        timer = 100
else:
    timer = -1

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
    blake2_hash = BLAKE2b.new()
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
    global frame, timer
    signature = sign_frame()
    if timer > 0:
        timer -= 1
    if timer != 0:
        return Response(frame.hex() + ',' + signature.hex(), mimetype='text/plain')
    else:
        return Response(signature.hex() + ',' + signature.hex(), mimetype='text/plain')

def cetak():
    warning = "\nPastikan port yang digunakan (default port 5000) dapat diakses oleh sistem\n"
    warning += "(Tidak diblokir oleh firewall dan tidak digunakan oleh proses lain)\n"
    warning += f"Apabila sistem tidak dapat diakses, ubah pengaturan firewall atau gunakan port lain seperti port {random.randint(1024, 49151)}\n"
    print(warning)
    print(f"Private IP: {private_ip}")
    print(f"Public IP: {public_ip}")

if __name__ == '__main__':
    # print(check_port())
    app.run(host='0.0.0.0', threaded=True)
cetak()