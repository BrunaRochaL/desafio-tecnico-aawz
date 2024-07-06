from sqlalchemy.orm import Session
from models.seller import Seller

class SellerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_seller_by_id(self, id: int):
        return self.db.query(Seller).filter(Seller.id == id).first()

    def get_seller_by_cpf(self, cpf: str):
        return self.db.query(Seller).filter(Seller.cpf == cpf).first()

    def create_seller(self, seller: Seller):
        self.db.add(seller)
        self.db.commit()
        self.db.refresh(seller)
        return seller

    def update_seller(self, seller: Seller):
        self.db.commit()
        self.db.refresh(seller)
        return seller

    def delete_seller(self, seller: Seller):
        self.db.delete(seller)
        self.db.commit()
        return True

    def get_all_sellers(self):
        return self.db.query(Seller).all()
