import sys
import socket
import subprocess
import platform

def is_port_available(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', port))
        return True
    except:
        return False

def start_gunicorn(port):
    if platform.system() == 'Windows':
        # On Windows, use the 'start' command to run Gunicorn in the background
        subprocess.Popen(f'start gunicorn --threads 6 --workers 1 --bind 0.0.0.0:{port} app:app --log-level=warning', shell=True)
    else:
        # On Linux, run Gunicorn directly
        subprocess.Popen(['gunicorn', '--threads', '6', '--workers', '1', f'--bind=0.0.0.0:{port}', 'app:app', '--log-level=warning'])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python helper.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    if is_port_available(port):
        print(f"Port {port} is available. Starting Gunicorn...")
        start_gunicorn(port)
    else:
        print(f"Port {port} is already in use. Cannot start Gunicorn.")