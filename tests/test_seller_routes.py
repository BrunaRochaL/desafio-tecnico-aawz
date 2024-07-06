import pytest
from flask import Flask
from database.database import init_db, SessionLocal
from models.seller import Base as SellerBase
from controllers.seller_controller import app as sellers_blueprint

@pytest.fixture(scope='module')
def test_app():
    app = Flask(__name__)
    app.register_blueprint(sellers_blueprint, url_prefix='/')

    with app.app_context():
        engine = SessionLocal().get_bind()
        SellerBase.metadata.create_all(engine)

    yield app

    with app.app_context():
        SellerBase.metadata.drop_all(engine)

@pytest.fixture
def client(test_app):
    return test_app.test_client()

def test_create_seller(client):
    seller_data = {
        "name": "Novo nome",
        "cpf": "04097026097",
        "birth_date": "01/01/2000",
        "email": "aaa@aaa.com",
        "state": "SP"
    }
    response = client.post('/sellers', json=seller_data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['cpf'] == "04097026097"
    assert json_data['name'] == "Novo nome"
    assert json_data['email'] == "aaa@aaa.com"
    assert json_data['state'] == "SP"

def test_get_seller(client):
    response = client.get('/sellers/cpf/04097026097')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['cpf'] == "04097026097"
    assert json_data['name'] == "Novo nome"
    assert json_data['email'] == "aaa@aaa.com"
    assert json_data['state'] == "SP"

def test_update_seller(client):
    update_data = {
        "name": "Nome Atualizado"
    }
    response = client.put('/sellers/1', json=update_data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['name'] == "Nome Atualizado"

def test_delete_seller(client):
    response = client.delete('/sellers/1')
    assert response.status_code == 204
    response = client.get('/sellers/1')
    assert response.status_code == 404
