import pytest
from io import BytesIO
from flask import Flask
from database.database import init_db, SessionLocal
from models.sale import Base as SaleBase
from models.seller import Base as SellerBase
from controllers.sale_controller import app as sales_blueprint
from controllers.seller_controller import app as sellers_blueprint

@pytest.fixture(scope='module')
def test_app():
    app = Flask(__name__)
    app.register_blueprint(sales_blueprint, url_prefix='/')
    app.register_blueprint(sellers_blueprint, url_prefix='/')

    with app.app_context():
        engine = SessionLocal().get_bind()
        SaleBase.metadata.create_all(engine)
        SellerBase.metadata.create_all(engine)

    yield app

    with app.app_context():
        SaleBase.metadata.drop_all(engine)
        SellerBase.metadata.drop_all(engine)

@pytest.fixture
def client(test_app):
    return test_app.test_client()

def create_seller(client):
    seller_data = {
        "name": "Novo nome",
        "cpf": "04097026097",
        "birth_date": "01/01/2000",
        "email": "aaa@aaa.com",
        "state": "SP"
    }
    client.post('/sellers', json=seller_data)

def test_calculate_commissions(client):
    create_seller(client)
    data = {
        'file': (BytesIO(b"CPF,Valor,Canal de Venda,Data,Tipo de Cliente,Moeda\n04097026097,1000,Online,2023-07-01 14:30:00,Novo,BRL"), 'sales.csv')
    }
    response = client.post('/commissions/calculate', content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert "04097026097" in json_data
    assert json_data["04097026097"] == 80.0

def test_get_sales_summary(client):
    response = client.get('/sales/summary')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'by_channel' in json_data
    assert 'by_state' in json_data
    assert 'by_client_type' in json_data

def test_get_sales_by_seller(client):
    response = client.get('/sales/04097026000')
    assert response.status_code == 404

def test_get_summary_by_seller(client):
    response = client.get('/sales/summary/04097026000')
    assert response.status_code == 404
