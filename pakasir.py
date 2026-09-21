"""
Helper integrasi Pakasir Payment Gateway.
Dokumentasi: https://pakasir.id / https://app.pakasir.com
"""
import os
import urllib.parse

def get_pakasir_checkout_url(order_id, amount, redirect_url=None):
    """
    Menghasilkan URL pembayaran Pakasir resmi.
    Format: https://app.pakasir.com/pay/{slug}/{amount}?order_id=...&redirect=...
    """
    slug = os.environ.get("PAKASIR_SLUG", "demo-saas")
    base_url = os.environ.get("PAKASIR_BASE_URL", "https://app.pakasir.com/pay").rstrip("/")
    
    url = f"{base_url}/{slug}/{amount}?order_id={urllib.parse.quote(order_id)}"
    if redirect_url:
        url += f"&redirect={urllib.parse.quote(redirect_url)}"
    return url

def verify_pakasir_webhook(data):
    """
    Validasi data webhook yang dikirimkan oleh server Pakasir.
    Payload contoh:
    {
        "amount": 50000,
        "order_id": "SAAS-1726912345",
        "project": "demo-saas",
        "status": "completed",
        "payment_method": "qris",
        "completed_at": "2026-09-21T10:00:00+07:00",
        "api_key": "..."
    }
    """
    if not data or not isinstance(data, dict):
        return False, "Payload data tidak valid"
    
    expected_slug = os.environ.get("PAKASIR_SLUG", "")
    expected_api_key = os.environ.get("PAKASIR_API_KEY", "")
    
    # 1. Validasi project slug
    project = data.get("project", "")
    if expected_slug and project != expected_slug:
        return False, f"Project mismatch: expected '{expected_slug}', got '{project}'"
    
    # 2. Validasi API key jika disertakan di payload
    payload_api_key = data.get("api_key", "")
    if expected_api_key and payload_api_key and payload_api_key != expected_api_key:
        return False, "API key signature tidak cocok"
    
    # 3. Validasi status
    status = data.get("status", "")
    if status != "completed":
        return False, f"Status bukan completed ({status})"
        
    return True, "Valid"
