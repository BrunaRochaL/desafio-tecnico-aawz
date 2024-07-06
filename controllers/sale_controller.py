from flask import Blueprint, request, jsonify, make_response
from database.database import SessionLocal
from services.sale_service import SaleService

app = Blueprint('sales', __name__)

@app.route('/commissions/calculate', methods=['POST'])
def calculate_commissions():
    db = SessionLocal()
    service = SaleService(db)
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        file_path = "/tmp/" + file.filename
        file.save(file_path)
        commissions = service.calculate_commissions(file_path)
        return jsonify(commissions)

@app.route('/sales/summary', methods=['GET'])
def get_sales_summary():
    db = SessionLocal()
    service = SaleService(db)
    summary = service.get_sales_summary()
    return jsonify(summary)

@app.route('/sales/<string:seller_cpf>', methods=['GET'])
def get_sales_by_seller(seller_cpf):
    db = SessionLocal()
    service = SaleService(db)
    sales = service.get_sales_by_seller(seller_cpf)
    if not sales:
        return make_response(jsonify({"error": "Seller not found"}), 404)
    return jsonify(sales)

@app.route('/sales/summary/<string:seller_cpf>', methods=['GET'])
def get_summary_by_seller(seller_cpf):
    db = SessionLocal()
    service = SaleService(db)
    summary = service.get_summary_by_seller(seller_cpf)
    if not summary:
        return make_response(jsonify({"error": "Seller not found"}), 404)
    return jsonify(summary)