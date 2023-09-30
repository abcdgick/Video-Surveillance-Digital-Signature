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

## Akses Melalui Internet

Agar sistem dapat diakses melalui internet, Anda dapat menggunakan layanan pihak ketiga seperti localtunnel (lt). Sebelum menjalankan server, jalankan perintah berikut agar localtunnel mengikat port yang digunakan server (default port 5000) :

```bash
lt --port 5000
```

#### Pastikan bahwa port yang akan digunakan oleh sistem (default port 5000) dapat diakses oleh sistem (tidak digunakan oleh aplikasi lain, tidak diblokir oleh firewall, dsb).
