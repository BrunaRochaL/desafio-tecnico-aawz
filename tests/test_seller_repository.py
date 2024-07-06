import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.seller import Seller, Base
from repositories.seller_repository import SellerRepository
from datetime import datetime

DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def repository(db):
    return SellerRepository(db)

def test_create_seller(repository):
    seller = Seller(
        name="Novo nome",
        cpf="04097026097",
        birth_date=datetime.strptime("01/01/2000", "%d/%m/%Y").date(),
        email="aaa@aaa.com",
        state="SP"
    )
    created_seller = repository.create_seller(seller)
    assert created_seller.id is not None
    assert created_seller.name == "Novo nome"
    assert created_seller.cpf == "04097026097"

def test_get_seller_by_id(repository):
    seller = Seller(
        name="Novo nome",
        cpf="04097026098",
        birth_date=datetime.strptime("01/01/2000", "%d/%m/%Y").date(),
        email="aaa2@aaa.com",
        state="SP"
    )
    created_seller = repository.create_seller(seller)
    fetched_seller = repository.get_seller_by_id(created_seller.id)
    assert fetched_seller is not None
    assert fetched_seller.id == created_seller.id

def test_get_seller_by_cpf(repository):
    seller = Seller(
        name="Novo nome",
        cpf="04097026099",
        birth_date=datetime.strptime("01/01/2000", "%d/%m/%Y").date(),
        email="aaa3@aaa.com",
        state="SP"
    )
    repository.create_seller(seller)
    fetched_seller = repository.get_seller_by_cpf("04097026099")
    assert fetched_seller is not None
    assert fetched_seller.cpf == "04097026099"

def test_update_seller(repository):
    seller = Seller(
        name="Novo nome",
        cpf="04097026100",
        birth_date=datetime.strptime("01/01/2000", "%d/%m/%Y").date(),
        email="aaa4@aaa.com",
        state="SP"
    )
    created_seller = repository.create_seller(seller)
    updated_data = {
        'name': "Nome Atualizado",
        'email': "atualizado@aaa.com"
    }
    for key, value in updated_data.items():
        setattr(created_seller, key, value)
    repository.update_seller(created_seller)
    updated_seller = repository.get_seller_by_id(created_seller.id)
    assert updated_seller.name == "Nome Atualizado"
    assert updated_seller.email == "atualizado@aaa.com"

def test_delete_seller(repository):
    seller = Seller(
        name="Novo nome",
        cpf="04097026101",
        birth_date=datetime.strptime("01/01/2000", "%d/%m/%Y").date(),
        email="aaa5@aaa.com",
        state="SP"
    )
    created_seller = repository.create_seller(seller)
    result = repository.delete_seller(created_seller)
    assert result
    fetched_seller = repository.get_seller_by_id(created_seller.id)
    assert fetched_seller is None

def test_get_all_sellers(repository):
    seller1 = Seller(
        name="Nome1",
        cpf="04097026102",
        birth_date=datetime.strptime("01/01/2000", "%d/%m/%Y").date(),
        email="aaa6@aaa.com",
        state="SP"
    )
    seller2 = Seller(
        name="Nome2",
        cpf="12345678901",
        birth_date=datetime.strptime("01/01/2001", "%d/%m/%Y").date(),
        email="bbb@bbb.com",
        state="RJ"
    )
    repository.create_seller(seller1)
    repository.create_seller(seller2)
    sellers = repository.get_all_sellers()
    assert len(sellers) >= 2
    assert sellers[0].name == "Nome1"
    assert sellers[1].name == "Nome2"
