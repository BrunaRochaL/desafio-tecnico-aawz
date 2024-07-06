import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.sale import Sale, Base as SaleBase
from models.seller import Seller, Base as SellerBase
from repositories.sale_repository import SaleRepository
from datetime import datetime

DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    SaleBase.metadata.create_all(engine)
    SellerBase.metadata.create_all(engine)
    session = Session()
    yield session
    session.close()
    SaleBase.metadata.drop_all(engine)
    SellerBase.metadata.drop_all(engine)

@pytest.fixture
def repository(db):
    return SaleRepository(db)

def test_save_sale(repository, db):
    seller = Seller(
        name="Seller Test",
        cpf="04097026097",
        birth_date=datetime.strptime("01/01/2000", "%d/%m/%Y").date(),
        email="test@seller.com",
        state="SP"
    )
    db.add(seller)
    db.commit()

    sale_data = {
        'seller_cpf': "04097026097",
        'value': 1000.0,
        'channel': "Online",
        'commission': 80.0,
        'date': datetime.strptime("2023-07-01 14:30:00", "%Y-%m-%d %H:%M:%S"),
        'client_type': "Novo",
        'currency': "BRL"
    }
    repository.save_sale(sale_data)
    saved_sale = db.query(Sale).filter(Sale.seller_cpf == "04097026097").first()

    assert saved_sale is not None
    assert saved_sale.value == 1000.0
    assert saved_sale.channel == "Online"
    assert saved_sale.commission == 80.0
    assert saved_sale.date == datetime.strptime("2023-07-01 14:30:00", "%Y-%m-%d %H:%M:%S")
    assert saved_sale.client_type == "Novo"
    assert saved_sale.currency == "BRL"

def test_get_sales_summary(repository, db):
    seller1 = Seller(
        name="Seller Test 1",
        cpf="04097026097",
        birth_date=datetime.strptime("01/01/2000", "%d/%m/%Y").date(),
        email="test1@seller.com",
        state="SP"
    )
    seller2 = Seller(
        name="Seller Test 2",
        cpf="04097026098",
        birth_date=datetime.strptime("01/01/2000", "%d/%m/%Y").date(),
        email="test2@seller.com",
        state="RJ"
    )
    db.add(seller1)
    db.add(seller2)
    db.commit()

    sale1 = Sale(
        seller_cpf="04097026097",
        value=1000.0,
        channel="Online",
        commission=80.0,
        date=datetime.strptime("2023-07-01 14:30:00", "%Y-%m-%d %H:%M:%S"),
        client_type="Novo",
        currency="BRL"
    )
    sale2 = Sale(
        seller_cpf="04097026098",
        value=2000.0,
        channel="Loja Física",
        commission=200.0,
        date=datetime.strptime("2023-07-01 15:00:00", "%Y-%m-%d %H:%M:%S"),
        client_type="Fidelizado",
        currency="BRL"
    )
    db.add(sale1)
    db.add(sale2)
    db.commit()

    sales_summary = repository.get_sales_summary()

    assert len(sales_summary) == 2
    assert sales_summary[0][0] == "04097026097"
    assert sales_summary[0][1] == "Online"
    assert sales_summary[0][2] == 1000.0
    assert sales_summary[0][3] == 80.0
    assert sales_summary[0][4] == "SP"
    assert sales_summary[0][5] == "Novo"

    assert sales_summary[1][0] == "04097026098"
    assert sales_summary[1][1] == "Loja Física"
    assert sales_summary[1][2] == 2000.0
    assert sales_summary[1][3] == 200.0
    assert sales_summary[1][4] == "RJ"
    assert sales_summary[1][5] == "Fidelizado"

def test_get_sales_by_seller(repository, db):
    seller = Seller(
        name="Seller Test",
        cpf="04097026097",
        birth_date=datetime.strptime("01/01/2000", "%d/%m/%Y").date(),
        email="test@seller.com",
        state="SP"
    )
    db.add(seller)
    db.commit()

    sale = Sale(
        seller_cpf="04097026097",
        value=1000.0,
        channel="Online",
        commission=80.0,
        date=datetime.strptime("2023-07-01 14:30:00", "%Y-%m-%d %H:%M:%S"),
        client_type="Novo",
        currency="BRL"
    )
    db.add(sale)
    db.commit()

    sales = repository.get_sales_by_seller("04097026097")

    assert len(sales) == 1
    assert sales[0].value == 1000.0
    assert sales[0].channel == "Online"
    assert sales[0].commission == 80.0
    assert sales[0].date == datetime.strptime("2023-07-01 14:30:00", "%Y-%m-%d %H:%M:%S")
    assert sales[0].client_type == "Novo"
    assert sales[0].currency == "BRL"
