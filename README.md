# Sistem Video Surveillance dengan Digital Signature

Sistem yang dibangun merupakan sistem video surveillance yang mengimplementasikan digital signature menggunakan RSA-PSS dan BLAKE2. Sistem ini menggunakan Flask server dan Gunicorn.

## Instalasi

Untuk menjalankan sistem ini, pastikan Anda telah menginstal semua library yang diperlukan yang terdapat dalam berkas `requirements.txt`. Anda dapat menginstalnya dengan menggunakan pip:

```bash
pip install -r requirements.txt
```

## Menjalankan Server

Untuk menjalankan server, gunakan perintah berikut:

```bash
gunicorn --threads 6 --workers 1 --bind 0.0.0.0:5000 app:app --log-level=warning
```

Untuk melakukan pengujian Digital Signature, set sys.argv[1] menjadi True:

```bash
gunicorn --threads 6 --workers 1 --bind 0.0.0.0:5000 app:app True --log-level=warning
```

## Akses Melalui Internet

Agar sistem dapat diakses melalui internet, Anda dapat menggunakan layanan pihak ketiga seperti ngrok. Sebelum menjalankan server, jalankan perintah berikut agar ngrok mengikat port yang digunakan server (default port 5000) :

```bash
ngrok http --domain=grateful-marlin-adversely.ngrok-free.app http://localhost:5000
```

#### Pastikan bahwa port yang akan digunakan (default port 5000) dapat diakses oleh sistem (tidak digunakan oleh aplikasi lain, tidak diblokir oleh firewall, dsb).
