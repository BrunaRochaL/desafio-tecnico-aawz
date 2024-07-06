import sys
import os
import pytest
from unittest.mock import MagicMock
from services.sale_service import SaleService
from models.sale import Sale
from models.seller import Seller
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def db():
    return MagicMock()

@pytest.fixture
def sale_service(db):
    return SaleService(db)

def test_calculate_commissions(sale_service):
    csv_content = """CPF,Valor,Canal de Venda,Data,Tipo de Cliente,Moeda
04097026097,1000,Online,2023-07-01 14:30:00,Novo,BRL
04097026098,2000,Loja Física,2023-07-01 15:00:00,Fidelizado,BRL
"""
    file_path = "/tmp/sales.csv"
    with open(file_path, "w") as f:
        f.write(csv_content)
    
    sale_service.seller_repository.get_seller_by_cpf = MagicMock(side_effect=[
        Seller(id=1, cpf="04097026097", name="Seller 1"),
        Seller(id=2, cpf="04097026098", name="Seller 2")
    ])
    sale_service.sale_repository.save_sale = MagicMock()
    
    commissions = sale_service.calculate_commissions(file_path)
    
    assert commissions == {
        "04097026097": 80.0, 
        "04097026098": 200.0 
    }

def test_calculate_commissions_with_errors(sale_service):
    csv_content = """CPF,Valor,Canal de Venda,Data,Tipo de Cliente,Moeda
04097026097,1000,Online,2023-07-01 14:30:00,Novo,BRL
04097026098,2000,Loja Física,2023-07-01 15:00:00,Fidelizado,BRL
"""
    file_path = "/tmp/sales_with_errors.csv"
    with open(file_path, "w") as f:
        f.write(csv_content)
    
    sale_service.seller_repository.get_seller_by_cpf = MagicMock(side_effect=[
        Seller(id=1, cpf="04097026097", name="Seller 1"),
        None
    ])
    sale_service.sale_repository.save_sale = MagicMock()
    
    result = sale_service.calculate_commissions(file_path)
    
    assert result['commissions'] == {
        "04097026097": 80.0 
    }
    assert len(result['errors']) == 1
    assert "Seller with CPF 04097026098 does not exist" in result['errors'][0]

def test_get_sales_summary(sale_service):
    sale_service.sale_repository.get_sales_summary = MagicMock(return_value=[
        ("04097026097", "Online", 1000.0, 80.0, "SP", "Novo"),
        ("04097026098", "Loja Física", 2000.0, 200.0, "RJ", "Fidelizado")
    ])
    
    summary = sale_service.get_sales_summary()
    assert summary == {
        'by_channel': {
            'Online': {
                'total_value': 1000.0,
                'total_commission': 80.0,
                'count': 1,
                'average_value': 1000.0,
                'average_commission': 80.0
            },
            'Loja Física': {
                'total_value': 2000.0,
                'total_commission': 200.0,
                'count': 1,
                'average_value': 2000.0,
                'average_commission': 200.0
            }
        },
        'by_seller': {
            "04097026097": {
                'total_value': 1000.0,
                'total_commission': 80.0,
                'count': 1,
                'average_value': 1000.0,
                'average_commission': 80.0
            },
            "04097026098": {
                'total_value': 2000.0,
                'total_commission': 200.0,
                'count': 1,
                'average_value': 2000.0,
                'average_commission': 200.0
            },
        },
        'by_state': {
            'SP': {
                'total_value': 1000.0,
                'total_commission': 80.0,
                'count': 1,
                'average_value': 1000.0,
                'average_commission': 80.0
            },
            'RJ': {
                'total_value': 2000.0,
                'total_commission': 200.0,
                'count': 1,
                'average_value': 2000.0,
                'average_commission': 200.0
            }
        },
        'by_client_type': {
            'Novo': {
                'total_value': 1000.0,
                'total_commission': 80.0,
                'count': 1,
                'average_value': 1000.0,
                'average_commission': 80.0
            },
            'Fidelizado': {
                'total_value': 2000.0,
                'total_commission': 200.0,
                'count': 1,
                'average_value': 2000.0,
                'average_commission': 200.0
            }
        }
    }

def test_get_sales_by_seller(sale_service):
    sale_service.seller_repository.get_seller_by_cpf = MagicMock(return_value=Seller(id=1, cpf="04097026097", name="Seller 1"))
    sale_service.sale_repository.get_sales_by_seller = MagicMock(return_value=[
        Sale(id=1, seller_cpf="04097026097", value=1000.0, channel="Online", commission=80.0, date=datetime.strptime("2023-07-01 14:30:00", "%Y-%m-%d %H:%M:%S"), client_type="Novo", currency="BRL"),
    ])
    
    sales = sale_service.get_sales_by_seller("04097026097")
    
    assert sales == [
        {
            'id': 1,
            'seller_cpf': "04097026097",
            'value': 1000.0,
            'channel': "Online",
            'commission': 80.0,
            'date': "2023-07-01 14:30:00",
            'client_type': "Novo",
            'currency': "BRL"
        }
    ]

def test_get_summary_by_seller(sale_service):
    sale_service.seller_repository.get_seller_by_cpf = MagicMock(return_value=Seller(id=1, cpf="04097026097", name="Seller 1"))
    sale_service.get_sales_by_seller = MagicMock(return_value=[
        {
            'id': 1,
            'seller_cpf': "04097026097",
            'value': 1000.0,
            'channel': "Online",
            'commission': 80.0,
            'date': "2023-07-01 14:30:00",
            'client_type': "Novo",
            'currency': "BRL"
        }
    ])
    
    summary = sale_service.get_summary_by_seller("04097026097")
    
    assert summary == {
        'seller_cpf': "04097026097",
        'total_value': 1000.0,
        'average_value': 1000.0,
        'total_commission': 80.0,
        'average_commission': 80.0,
        'sales': [
            {
                'id': 1,
                'seller_cpf': "04097026097",
                'value': 1000.0,
                'channel': "Online",
                'commission': 80.0,
                'date': "2023-07-01 14:30:00",
                'client_type': "Novo",
                'currency': "BRL"
            }
        ]
    }
