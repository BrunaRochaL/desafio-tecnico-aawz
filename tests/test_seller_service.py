from unittest.mock import MagicMock
from services.seller_service import SellerService
from models.seller import Seller
from datetime import datetime, date

def test_create_seller():
    db = MagicMock()
    service = SellerService(db)
    
    service.repository.get_seller_by_cpf = MagicMock(return_value=None)
    service.repository.create_seller = MagicMock(return_value=Seller(
        id=1, name="Novo nome", cpf="04097026097", birth_date=date(2000, 1, 1), email="aaa@aaa.com", state="SP"
    ))

    seller_data = {
        "name": "Novo nome",
        "cpf": "04097026097",
        "birth_date": "01/01/2000",
        "email": "aaa@aaa.com",
        "state": "SP"
    }

    seller = service.create_seller(**seller_data)
    
    assert seller["name"] == "Novo nome"
    assert seller["cpf"] == "04097026097"
    assert seller["email"] == "aaa@aaa.com"

def test_create_seller_with_existing_cpf():
    db = MagicMock()
    service = SellerService(db)
    
    service.repository.get_seller_by_cpf = MagicMock(return_value=Seller(
        id=1, name="Existing name", cpf="04097026097", birth_date=date(2000, 1, 1), email="existing@aaa.com", state="SP"
    ))

    seller_data = {
        "name": "Novo nome",
        "cpf": "04097026097",
        "birth_date": "01/01/2000",
        "email": "aaa@aaa.com",
        "state": "SP"
    }

    seller = service.create_seller(**seller_data)
    
    assert "error" in seller
    assert seller["error"] == "CPF already exists"

def test_update_seller():
    db = MagicMock()
    service = SellerService(db)
    
    existing_seller = Seller(id=1, name="Existing name", cpf="04097026097", birth_date=date(2000, 1, 1), email="existing@aaa.com", state="SP")
    service.repository.get_seller_by_id = MagicMock(return_value=existing_seller)
    service.repository.update_seller = MagicMock(return_value=existing_seller)

    update_data = {
        "name": "Updated name"
    }

    updated_seller = service.update_seller(1, update_data)
    
    assert updated_seller["name"] == "Updated name"
    assert updated_seller["cpf"] == "04097026097"

def test_update_seller_invalid_cpf():
    db = MagicMock()
    service = SellerService(db)
    
    existing_seller = Seller(id=1, name="Existing name", cpf="04097026097", birth_date=date(2000, 1, 1), email="existing@aaa.com", state="SP")
    service.repository.get_seller_by_id = MagicMock(return_value=existing_seller)

    update_data = {
        "cpf": "12345678901"
    }

    updated_seller = service.update_seller(1, update_data)
    
    assert "error" in updated_seller
    assert updated_seller["error"] == "Invalid CPF"

def test_delete_seller():
    db = MagicMock()
    service = SellerService(db)
    
    existing_seller = Seller(id=1, name="Existing name", cpf="04097026097", birth_date=date(2000, 1, 1), email="existing@aaa.com", state="SP")
    service.repository.get_seller_by_id = MagicMock(return_value=existing_seller)
    service.repository.delete_seller = MagicMock(return_value=True)

    success = service.delete_seller(1)
    
    assert success

def test_load_sellers_from_csv():
    db = MagicMock()
    service = SellerService(db)

    service.repository.get_seller_by_cpf = MagicMock(return_value=None)
    service.repository.create_seller = MagicMock()

    csv_content = """Nome,CPF,Data de Nascimento,Email,Estado
Alice Silva,25653370002,01/01/1980,alice.silva@example.com,SP
Bruno Costa,83177313083,15/05/1985,bruno.costa@example.com,RJ
"""

    with open("/tmp/sellers.csv", "w") as f:
        f.write(csv_content)

    result = service.load_sellers_from_csv("/tmp/sellers.csv")
    assert "errors" not in result
    assert result["message"] == "Sellers loaded successfully"
