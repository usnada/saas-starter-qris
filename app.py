import os
import json
import time
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from dotenv import load_dotenv

from models import init_db, create_order, get_order, mark_order_completed, is_user_active
from pakasir import get_pakasir_checkout_url, verify_pakasir_webhook

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-12345")

# Support subpath routing (misal: /demo-saas/)
class PrefixMiddleware:
    def __init__(self, wsgi_app, prefix=""):
        self.wsgi_app = wsgi_app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        prefix = environ.get("HTTP_X_FORWARDED_PREFIX") or self.prefix
        if prefix:
            environ["SCRIPT_NAME"] = prefix
            path_info = environ.get("PATH_INFO", "")
            if path_info.startswith(prefix):
                environ["PATH_INFO"] = path_info[len(prefix):] or "/"
        return self.wsgi_app(environ, start_response)

app_prefix = os.environ.get("APP_PREFIX", "")
if app_prefix or os.path.exists("/etc/systemd/system/saas-demo.service"):
    # Default prefix untuk instance live demo
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=app_prefix or "/demo-saas")

# Initialize database
init_db()

PLANS = {
    "starter": {
        "name": "Starter Plan",
        "price": 49000,
        "features": [
            "Akses Fitur Dasar SaaS",
            "1 Project Aktif",
            "Dukungan Email Komunitas",
            "Akses Seumur Hidup (LTD)"
        ]
    },
    "pro": {
        "name": "Pro Developer",
        "price": 149000,
        "features": [
            "Semua Fitur Starter",
            "Unlimited Project",
            "Source Code Lengkap",
            "Dukungan Prioritas 24/7",
            "Gratis Update Selamanya"
        ]
    }
}

@app.route("/")
def index():
    user_email = session.get("user_email")
    has_active_sub = is_user_active(user_email) if user_email else False
    return render_template("index.html", plans=PLANS, user_email=user_email, has_active_sub=has_active_sub)

@app.route("/checkout/<plan_id>", methods=["GET", "POST"])
def checkout(plan_id):
    if plan_id not in PLANS:
        flash("Paket langganan tidak valid.", "danger")
        return redirect(url_for("index"))
    
    plan = PLANS[plan_id]
    
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if not email or "@" not in email:
            flash("Mohon masukkan alamat email yang valid.", "warning")
            return render_template("checkout.html", plan_id=plan_id, plan=plan)
        
        # Simpan sesi login sederhana
        session["user_email"] = email
        
        # Buat Order ID unik
        order_id = f"SAAS-{int(time.time())}-{os.urandom(3).hex().upper()}"
        create_order(order_id, email, plan["name"], plan["price"])
        
        # URL redirect setelah user membayar di halaman Pakasir
        app_url = os.environ.get("APP_URL", request.host_url.rstrip("/"))
        redirect_url = f"{app_url}/payment/success?order_id={order_id}"
        
        # Dapatkan URL pembayaran Pakasir (langsung QRIS)
        checkout_url = get_pakasir_checkout_url(order_id, plan["price"], redirect_url, qris_only=True)
        return redirect(checkout_url)
        
    return render_template("checkout.html", plan_id=plan_id, plan=plan)

@app.route("/payment/webhook", methods=["POST"])
def webhook():
    """
    Endpoint Webhook untuk menerima konfirmasi pembayaran instan dari Pakasir.
    """
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Missing JSON payload"}), 400
    
    is_valid, msg = verify_pakasir_webhook(payload)
    if not is_valid:
        app.logger.warning(f"Webhook rejected: {msg} | Payload: {payload}")
        return jsonify({"error": msg}), 400
    
    order_id = payload.get("order_id")
    order = get_order(order_id)
    if not order:
        return jsonify({"error": "Order tidak ditemukan"}), 404
        
    payment_method = payload.get("payment_method", "qris")
    mark_order_completed(order_id, payment_method, json.dumps(payload))
    
    app.logger.info(f"Pembayaran Order {order_id} BERHASIL diverifikasi via Webhook Pakasir.")
    return jsonify({"status": "success", "message": "Order completed"}), 200

@app.route("/payment/success")
def payment_success():
    order_id = request.args.get("order_id", "")
    order = get_order(order_id) if order_id else None
    return render_template("success.html", order=order)

@app.route("/download/<order_id>")
def download_file(order_id):
    """
    Endpoint proteksi unduhan:
    Hanya mengizinkan unduhan jika order_id benar-benar berstatus 'completed' (sudah lunas).
    """
    order = get_order(order_id)
    if not order:
        flash("Pesanan tidak ditemukan.", "danger")
        return redirect(url_for("index"))
        
    if order["status"] != "completed":
        flash("⛔ Pembayaran belum terkonfirmasi lunas. Silakan selesaikan pembayaran terlebih dahulu.", "warning")
        return redirect(url_for("payment_success", order_id=order_id))
        
    # Kirim file zip produk
    from flask import send_from_directory
    projects_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = "saas-starter-qris-v1.0.0.zip"
    if not os.path.exists(os.path.join(projects_dir, filename)):
        projects_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(projects_dir, filename, as_attachment=True)

@app.route("/api/order-status/<order_id>")
def order_status(order_id):
    order = get_order(order_id)
    if not order:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "order_id": order["order_id"],
        "status": order["status"],
        "plan_name": order["plan_name"]
    })

@app.route("/dashboard")
def dashboard():
    email = session.get("user_email")
    if not email:
        flash("Silakan masukkan email atau lakukan pembelian terlebih dahulu.", "info")
        return redirect(url_for("login"))
        
    if not is_user_active(email):
        flash("Akun Anda belum memiliki paket aktif. Pilih paket untuk mulai.", "warning")
        return redirect(url_for("index"))
        
    return render_template("dashboard.html", user_email=email)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if email and "@" in email:
            session["user_email"] = email
            if is_user_active(email):
                return redirect(url_for("dashboard"))
            flash("Email terdaftar belum memiliki langganan aktif. Silakan pilih paket.", "info")
            return redirect(url_for("index"))
        flash("Format email tidak valid.", "warning")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_email", None)
    flash("Anda telah logout.", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "True").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
