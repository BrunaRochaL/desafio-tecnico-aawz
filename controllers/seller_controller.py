from flask import Blueprint, request, jsonify, abort, make_response
from database.database import SessionLocal
from services.seller_service import SellerService

app = Blueprint('sellers', __name__)

@app.route('/sellers/<int:id>', methods=['GET'])
def get_seller(id):
    db = SessionLocal()
    service = SellerService(db)
    seller = service.get_seller(id)
    if seller is None:
        return make_response(jsonify({"error": "Seller not found"}), 404)
    return jsonify(seller)

@app.route('/sellers/cpf/<cpf>', methods=['GET'])
def get_seller_by_cpf(cpf):
    db = SessionLocal()
    service = SellerService(db)
    seller = service.get_seller_by_cpf(cpf)
    if seller is None:
        return make_response(jsonify({"error": "Seller not found"}), 404)
    return jsonify(seller)

@app.route('/sellers', methods=['POST'])
def create_seller():
    db = SessionLocal()
    service = SellerService(db)
    data = request.json

    required_fields = ["name", "cpf", "birth_date", "email", "state"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return make_response(jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400)

    seller = service.create_seller(
        name=data['name'],
        cpf=data['cpf'],
        birth_date=data['birth_date'],
        email=data['email'],
        state=data['state']
    )
    if 'error' in seller:
        return make_response(jsonify(seller), 400)
    return jsonify(seller), 201

@app.route('/sellers/<int:id>', methods=['PUT'])
def update_seller(id):
    db = SessionLocal()
    service = SellerService(db)
    data = request.json

    if not data:
        return make_response(jsonify({"error": "At least one field must be provided"}), 400)

    seller = service.update_seller(id, data)
    if seller is None:
        return make_response(jsonify({"error": "Seller not found"}), 404)
    if 'error' in seller:
        return make_response(jsonify(seller), 400)
    return jsonify(seller)

@app.route('/sellers/<int:id>', methods=['DELETE'])
def delete_seller(id):
    db = SessionLocal()
    service = SellerService(db)
    success = service.delete_seller(id)
    if not success:
        return make_response(jsonify({"error": "Seller not found"}), 404)
    return '', 204

@app.route('/sellers', methods=['GET'])
def get_all_sellers():
    db = SessionLocal()
    service = SellerService(db)
    sellers = service.get_all_sellers()
    return jsonify(sellers)

@app.route('/sellers/load', methods=['POST'])
def load_sellers():
    db = SessionLocal()
    service = SellerService(db)
    file = request.files['file']
    file_path = "/tmp/" + file.filename
    file.save(file_path)
    result = service.load_sellers_from_csv(file_path)
    if 'errors' in result:
        return make_response(jsonify(result), 400)
    return jsonify(result)
