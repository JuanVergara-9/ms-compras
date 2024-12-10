from flask import Blueprint, request, jsonify
from app.services import CompraService
from tenacity import retry
from tenacity.wait import wait_fixed
from tenacity.stop import stop_after_attempt

compra = Blueprint('compra', __name__)

@compra.route('/compra/add', methods=['POST'])
@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5))
def add_compra():
    data = request.get_json()
    response, status = CompraService.add_compra(data)
    return jsonify(response), status

@compra.route('/compra/remove', methods=['POST'])
@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5))
def remove_compra():
    data = request.get_json()
    response, status = CompraService.remove_compra(data)
    return jsonify(response), status