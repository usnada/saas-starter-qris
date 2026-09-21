# ⚡ SaaS Starter Kit Indonesia (Flask + QRIS Pakasir) — Production Ready

**Luncurkan SaaS Lokal Anda Dalam Hitungan Jam, Bukan Minggu!**

Capek menghabiskan waktu 2-3 minggu hanya untuk mengatur sistem otentikasi, mendesain halaman checkout, dan menghubungkan webhook pembayaran? 

Gunakan **SaaS Starter Kit Indonesia** berbasis **Python Flask**. Boilerplate siap produksi ini dirancang khusus bagi developer solo, freelancer, dan indie hacker yang ingin langsung berjualan produk digital atau layanan SaaS berlangganan dengan sistem pembayaran **QRIS otomatis (Pakasir)**.

---

### 🌟 Fitur Unggulan

1. **💳 Pembayaran QRIS Otomatis:**
   - Terintegrasi langsung dengan gateway Pakasir (BCA, Mandiri, BRI, BNI, GoPay, OVO, Dana, ShopeePay).
   - Webhook listener real-time: status order langsung otomatis `completed` seketika saat pembeli selesai scan QRIS.
2. **🔒 Manajemen Sesi & Proteksi Member:**
   - Sistem login email sederhana tanpa beban konfigurasi rumit.
   - Area `/dashboard` otomatis terkunci dan hanya bisa diakses oleh pelanggan dengan pesanan lunas.
3. **🗄️ Database Ringan (Zero-Config SQLite):**
   - Tidak perlu install MySQL atau PostgreSQL terpisah. Database siap jalan otomatis begitu aplikasi pertama kali dijalankan.
4. **🎨 UI Modern & Responsif (Dark Mode):**
   - Halaman Beranda / Landing Page + Tabel Harga 2 Tier (Starter & Pro).
   - Halaman Checkout, Konfirmasi Sukses, dan Dashboard Anggota dengan desain profesional.
5. **🚀 Siap Deploy ke Linux/VPS:**
   - Disertai contoh konfigurasi Gunicorn & Nginx reverse proxy untuk online dalam 5 menit.

---

### 📦 Apa yang Anda Dapatkan?

- Source Code lengkap (Python Flask, HTML, CSS modern).
- Berkas template konfigurasi `.env.example` dan schema database SQLite.
- File dokumentasi panduan setup lokal hingga live di VPS (`README.md`).
- Lisensi komersial penuh (Bebas dipakai untuk proyek pribadi maupun klien tanpa batas!).

---

### 🔗 Live Demo Online
Coba langsung demonya di browser Anda:
👉 **https://usnada.com/demo-saas/**

---

### 💡 Cocok Untuk Siapa?
- Developer yang ingin validasi ide SaaS berbayar dengan cepat di pasar Indonesia.
- Freelancer yang sering membuatkan website membership / portal berbayar untuk klien.
- Pembuat tools micro-SaaS berbasis AI atau otomasi.
