from sqlalchemy.orm import Session
from models.sale import Sale
from models.seller import Seller

class SaleRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_sale(self, sale_data):
        sale = Sale(
            seller_cpf=sale_data['seller_cpf'],
            value=sale_data['value'],
            channel=sale_data['channel'],
            commission=sale_data['commission'],
            date=sale_data['date'],
            client_type=sale_data['client_type'],
            currency=sale_data['currency']
        )
        self.db.add(sale)
        self.db.commit()

    def get_sales_summary(self):
        sales_summary = self.db.query(
            Sale.seller_cpf,
            Sale.channel,
            Sale.value,
            Sale.commission,
            Seller.state,            
            Sale.client_type
        ).join(Seller, Sale.seller_cpf == Seller.cpf).all()

        return sales_summary

    def get_sales_by_seller(self, seller_cpf):
        return self.db.query(Sale).filter(Sale.seller_cpf == seller_cpf).all()
