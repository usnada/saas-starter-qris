# ⚡ SaaS Starter Kit Indonesia (Flask + Pakasir QRIS)

![SaaS Starter Kit Indonesia Cover](https://usnada.com/product_cover.png)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Online-brightgreen?style=for-the-badge&logo=googlechrome)](https://usnada.com/demo-saas/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-Commercial%20Ready-orange?style=for-the-badge)](https://payhip.com)

**Luncurkan Produk SaaS Lokal Anda Dalam Hitungan Jam, Bukan Minggu!**

Boilerplate SaaS lengkap siap produksi berbasis **Python Flask**, terintegrasi dengan **Payment Gateway QRIS Pakasir**, otentikasi sesi anggota, dan manajemen database SQLite ringan tanpa ribet.

---

## 🔗 Coba Live Demo
Akses demo langsung di browser:
👉 **[https://usnada.com/demo-saas/](https://usnada.com/demo-saas/)**

---

## ✨ Fitur Utama

- 💳 **Pembayaran QRIS Otomatis:** Integrasi instan dengan Pakasir (BCA, Mandiri, BRI, BNI, GoPay, OVO, ShopeePay, Dana).
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
├── PANDUAN_PEMBELI.txt   # Panduan instalasi cepat bagi pembeli
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

## 🛒 Dapatkan Source Code Lengkap

Anda bisa mendapatkan source code lengkap siap pakai, file `.env.example`, dan hak lisensi komersial seumur hidup:

- 🇮🇩 **[Beli di Lynk.id (QRIS / Bank Transfer / E-Wallet)](https://lynk.id](http://lynk.id/usnada/olq85jz6wlk8/checkout)**
- 🌍 **[Beli di Payhip (PayPal / Kartu Kredit Global)](https://payhip.com)](https://payhip.com/b/v5xRc)**

*(File `.zip` langsung terkirim otomatis dan dapat diunduh seketika setelah pembayaran).*

## 🛠️ Panduan Instalasi Cepat (Bagi Pemilik Lisensi)

1. **Ekstrak & Install Dependensi:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Setup File `.env`:**
   ```bash
   cp .env.example .env
   ```
   Isi `PAKASIR_SLUG` dan `PAKASIR_API_KEY` dari dashboard [Pakasir.id](https://pakasir.id).

3. **Jalankan Aplikasi:**
   ```bash
   python3 app.py
   ```
   Buka `http://localhost:5000` di browser Anda.

---

## 📄 Lisensi

Lisensi Komersial: Bebas digunakan untuk membangun aplikasi SaaS pribadi maupun proyek klien tanpa batas. Dilarang mendistribusikan atau menjual ulang source code mentah ini sebagai produk template di platform lain.

Dibuat dengan ❤️ oleh [I Ketut Usnada](https://usnada.com)
