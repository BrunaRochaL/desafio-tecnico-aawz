import re
from sqlalchemy.orm import Session
from models.seller import Seller
from repositories.seller_repository import SellerRepository
from utils.document_utils import is_valid_cpf
from utils.email_utils import is_valid_email
from datetime import datetime
import pandas as pd

VALID_STATES = {"AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"}

class SellerService:
    def __init__(self, db: Session):
        self.repository = SellerRepository(db)

    def get_seller(self, id: int):
        seller = self.repository.get_seller_by_id(id)
        return self.to_dict(seller) if seller else None

    def get_seller_by_cpf(self, cpf: str):
        seller = self.repository.get_seller_by_cpf(cpf)
        return self.to_dict(seller) if seller else None

    def create_seller(self, name, cpf, birth_date, email, state):
        cpf = ''.join(filter(str.isdigit, str(cpf))).zfill(11)
        if not is_valid_cpf(cpf):
            return {"error": "Invalid CPF"}
        if not is_valid_email(email):
            return {"error": "Invalid email format"}
        if state not in VALID_STATES:
            return {"error": "Invalid state abbreviation"}
        if self.repository.get_seller_by_cpf(cpf):
            return {"error": "CPF already exists"}
        birth_date = datetime.strptime(birth_date, "%d/%m/%Y").date()
        seller = Seller(name=name, cpf=cpf, birth_date=birth_date, email=email, state=state)
        created_seller = self.repository.create_seller(seller)
        return self.to_dict(created_seller)

    def update_seller(self, id: int, data: dict):
        seller = self.repository.get_seller_by_id(id)
        if not seller:
            return None

        if 'cpf' in data:
            data['cpf'] = ''.join(filter(str.isdigit, str(data['cpf']))).zfill(11)
            if not is_valid_cpf(data['cpf']):
                return {"error": "Invalid CPF"}
            if data['cpf'] != seller.cpf and self.repository.get_seller_by_cpf(data['cpf']):
                return {"error": "CPF already exists"}
        
        if 'email' in data and not is_valid_email(data['email']):
            return {"error": "Invalid email format"}

        if 'state' in data and data['state'] not in VALID_STATES:
            return {"error": "Invalid state abbreviation"}

        for key, value in data.items():
            if key == 'birth_date':
                value = datetime.strptime(value, "%d/%m/%Y").date()
            setattr(seller, key, value)
        updated_seller = self.repository.update_seller(seller)
        return self.to_dict(updated_seller)

    def delete_seller(self, id: int):
        seller = self.repository.get_seller_by_id(id)
        if not seller:
            return False
        self.repository.delete_seller(seller)
        return True

    def get_all_sellers(self):
        sellers = self.repository.get_all_sellers()
        return [self.to_dict(seller) for seller in sellers]

    def load_sellers_from_csv(self, file_path: str):
        df = pd.read_csv(file_path)
        errors = []

        for _, row in df.iterrows():
            seller_data = {
                'name': row['Nome'],
                'cpf': ''.join(filter(str.isdigit, str(row['CPF']))).zfill(11),
                'birth_date': row['Data de Nascimento'],
                'email': row['Email'],
                'state': row['Estado']
            }

            if not is_valid_cpf(seller_data['cpf']):
                errors.append(f"Invalid CPF: {seller_data['cpf']}")
                continue

            if not is_valid_email(seller_data['email']):
                errors.append(f"Invalid email: {seller_data['email']}")
                continue

            if seller_data['state'] not in VALID_STATES:
                errors.append(f"Invalid state abbreviation: {seller_data['state']}")
                continue

            existing_seller = self.repository.get_seller_by_cpf(seller_data['cpf'])
            if existing_seller:
                self.update_seller(existing_seller.id, seller_data)
            else:
                self.create_seller(**seller_data)

        if errors:
            return {"errors": errors}
        return {"message": "Sellers loaded successfully"}

    def to_dict(self, seller: Seller):
        if not seller:
            return None
        return {
            'id': seller.id,
            'cpf': seller.cpf,
            'name': seller.name,
            'birth_date': seller.birth_date.strftime("%d/%m/%Y"),
            'email': seller.email,
            'state': seller.state
        }
