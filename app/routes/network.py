from flask import Blueprint, request
from app.utils.cmd import ping_address_vulnerable, ping_address_safe

network_bp = Blueprint('network', __name__)

@network_bp.route('/ping', methods=['POST'])
def ping_unsafe():
    address = request.form.get('address')
    result = ping_address_vulnerable(address)
    return f"Ping Result (Unsafe):<br><pre>{result}</pre><br><a href='/'>Back</a>"

@network_bp.route('/ping_safe', methods=['POST'])
def ping_safe():
    address = request.form.get('address')
    result = ping_address_safe(address)
    return f"Ping Result (Safe):<br><pre>{result}</pre><br><a href='/'>Back</a>"
