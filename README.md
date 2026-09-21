# ⚡ SaaS Starter Kit Indonesia (Flask + Pakasir QRIS)

Boilerplate SaaS lengkap siap produksi berbasis **Python Flask**, terintegrasi dengan **Payment Gateway QRIS Pakasir**, otentikasi sesi, dan manajemen database SQLite ringan. 

Dirancang khusus bagi developer, solo founder, dan kreator digital yang ingin meluncurkan produk SaaS berbayar di pasar Indonesia dalam hitungan jam tanpa harus membangun sistem pembayaran dari nol.

---

## ✨ Fitur Utama

- 💳 **Pembayaran QRIS Otomatis:** Integrasi instan dengan Pakasir (BCA, Mandiri, BRI, GoPay, OVO, ShopeePay, Dana).
- 🔄 **Webhook Verifikasi Real-Time:** Status pesanan langsung menjadi `completed` seketika saat pembeli scan QRIS.
- 🔒 **Sistem Sesi & Akses Anggota:** Membatasi akses `/dashboard` hanya untuk pembeli yang memiliki transaksi aktif.
- 🗄️ **Zero-Config Database:** Menggunakan SQLite bawaan Python, tidak perlu install server MySQL/PostgreSQL tambahan.
- 🎨 **UI Modern & Responsif:** Desain dark mode elegan yang sudah disiapkan untuk landing page, checkout, dan dashboard.
- 🚀 **Production-Ready:** Siap dideploy menggunakan Gunicorn dan Nginx di Linux/Ubuntu VPS.

---

## 📁 Struktur Direktori

```text
saas-starter-qris/
├── app.py                # Core aplikasi Flask & router endpoints
├── models.py             # Database helper & schema SQLite
├── pakasir.py            # Helper URL generator & verifikasi webhook Pakasir
├── requirements.txt      # Dependensi Python
├── .env.example          # Contoh variabel lingkungan
├── database.sqlite       # Database SQLite lokal (dibuat otomatis)
├── static/
│   └── style.css         # Styling modern dark mode
└── templates/
    ├── base.html         # Template induk navbar & layout
    ├── index.html        # Landing page & pricing table
    ├── checkout.html     # Halaman input email & ringkasan order
    ├── success.html      # Konfirmasi pembayaran sukses
    ├── dashboard.html    # Area privat member aktif
    └── login.html        # Form login anggota
```

---

## 🛠️ Panduan Instalasi Cepat

### 1. Clone & Setup Environment
```bash
git clone https://github.com/username/saas-starter-qris.git
cd saas-starter-qris

# Buat virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependensi
pip install -r requirements.txt
```

### 2. Konfigurasi Variabel Lingkungan (`.env`)
Salin file `.env.example` menjadi `.env`:
```bash
cp .env.example .env
```

Buka dan sesuaikan nilainya:
```ini
SECRET_KEY=kunci_rahasia_acak_yang_panjang
PORT=5000
DEBUG=True

# Dapatkan dari dashboard https://pakasir.id
PAKASIR_SLUG=proyek-saas-anda
PAKASIR_API_KEY=api_key_dari_pakasir
PAKASIR_BASE_URL=https://app.pakasir.com/pay

APP_URL=http://localhost:5000
```

### 3. Jalankan Aplikasi Lokal
```bash
python3 app.py
```
Buka browser di `http://localhost:5000`.

---

## 🔗 Menghubungkan Webhook Pakasir

1. Masuk ke dashboard [Pakasir.id](https://pakasir.id).
2. Di pengaturan proyek Anda, masukkan **Webhook URL**:
   `https://domain-anda.com/payment/webhook`
3. Setiap kali transaksi QRIS berhasil, server Pakasir akan mengirimkan payload JSON ke endpoint ini dan sistem secara otomatis mengaktifkan status akun pembeli.

---

## 🚀 Panduan Deploy ke VPS (Ubuntu + Nginx)

Jalankan server produksi menggunakan Gunicorn:
```bash
gunicorn -w 3 -b 127.0.0.1:5000 app:app
```

Contoh konfigurasi Nginx reverse proxy:
```nginx
server {
    server_name saas-anda.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 📄 Lisensi

MIT License. Bebas digunakan untuk keperluan komersial, personal, maupun sebagai fondasi startup SaaS Anda.
