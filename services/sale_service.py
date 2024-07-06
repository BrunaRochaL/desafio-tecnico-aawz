from sqlalchemy.orm import Session
from models.sale import Sale
from repositories.sale_repository import SaleRepository
from repositories.seller_repository import SellerRepository
from datetime import datetime
import pandas as pd

class SaleService:
    def __init__(self, db: Session):
        self.sale_repository = SaleRepository(db)
        self.seller_repository = SellerRepository(db)

    def calculate_commissions(self, sales_file_path: str):
        df = pd.read_csv(sales_file_path, dtype={'CPF': str})
        commissions = {}
        sales = []
        errors = []

        for _, row in df.iterrows():
            cpf = row['CPF']
            seller = self.seller_repository.get_seller_by_cpf(cpf)
            if not seller:
                errors.append(f"Seller with CPF {cpf} does not exist for sale on {row['Data']}.")
                continue

            value = float(row['Valor'])
            channel = row['Canal de Venda']
            date = datetime.strptime(row['Data'], "%Y-%m-%d %H:%M:%S")
            client_type = row['Tipo de Cliente']
            currency = row['Moeda']

            commission = value * 0.10
            if channel == 'Online':
                commission *= 0.80

            sales.append({
                'seller_cpf': cpf,
                'value': value,
                'channel': channel,
                'commission': commission,
                'date': date,
                'client_type': client_type,
                'currency': currency
            })

            if cpf not in commissions:
                commissions[cpf] = 0
            commissions[cpf] += commission

        for sale in sales:
            self.sale_repository.save_sale(sale)

        final_commissions = {}
        for cpf, total_commission in commissions.items():
            if total_commission >= 1000:
                final_commission = total_commission * 0.90
            else:
                final_commission = total_commission
            final_commissions[cpf] = final_commission

        if errors:
            return {'errors': errors, 'commissions': final_commissions}
        return final_commissions

    def get_sales_summary(self):
        summary = self.sale_repository.get_sales_summary()

        summary_by_channel = {}
        summary_by_state = {}
        summary_by_client_type = {}
        summary_by_seller = {}

        for sale in summary:
            cpf, channel, value, commission, state, client_type = sale

            if channel not in summary_by_channel:
                summary_by_channel[channel] = {'total_value': 0, 'total_commission': 0, 'count': 0}
            summary_by_channel[channel]['total_value'] += value
            summary_by_channel[channel]['total_commission'] += commission
            summary_by_channel[channel]['count'] += 1

            if state not in summary_by_state:
                summary_by_state[state] = {'total_value': 0, 'total_commission': 0, 'count': 0}
            summary_by_state[state]['total_value'] += value
            summary_by_state[state]['total_commission'] += commission
            summary_by_state[state]['count'] += 1

            if client_type not in summary_by_client_type:
                summary_by_client_type[client_type] = {'total_value': 0, 'total_commission': 0, 'count': 0}
            summary_by_client_type[client_type]['total_value'] += value
            summary_by_client_type[client_type]['total_commission'] += commission
            summary_by_client_type[client_type]['count'] += 1

            if cpf not in summary_by_seller:
                summary_by_seller[cpf] = {'total_value': 0, 'total_commission': 0, 'count': 0}
            summary_by_seller[cpf]['total_value'] += value
            summary_by_seller[cpf]['total_commission'] += commission
            summary_by_seller[cpf]['count'] += 1

        for channel in summary_by_channel:
            summary_by_channel[channel]['average_value'] = round(summary_by_channel[channel]['total_value'] / summary_by_channel[channel]['count'], 2)
            summary_by_channel[channel]['average_commission'] = round(summary_by_channel[channel]['total_commission'] / summary_by_channel[channel]['count'], 2)

        for state in summary_by_state:
            summary_by_state[state]['average_value'] = round(summary_by_state[state]['total_value'] / summary_by_state[state]['count'], 2)
            summary_by_state[state]['average_commission'] = round(summary_by_state[state]['total_commission'] / summary_by_state[state]['count'], 2)

        for client_type in summary_by_client_type:
            summary_by_client_type[client_type]['average_value'] = round(summary_by_client_type[client_type]['total_value'] / summary_by_client_type[client_type]['count'], 2)
            summary_by_client_type[client_type]['average_commission'] = round(summary_by_client_type[client_type]['total_commission'] / summary_by_client_type[client_type]['count'], 2)

        for cpf in summary_by_seller:
            summary_by_seller[cpf]['average_value'] = round(summary_by_seller[cpf]['total_value'] / summary_by_seller[cpf]['count'], 2)
            summary_by_seller[cpf]['average_commission'] = round(summary_by_seller[cpf]['total_commission'] / summary_by_seller[cpf]['count'], 2)

        return {
            'by_channel': summary_by_channel,
            'by_state': summary_by_state,
            'by_client_type': summary_by_client_type,
            'by_seller': summary_by_seller
        }

    def get_sales_by_seller(self, seller_cpf):
        seller = self.seller_repository.get_seller_by_cpf(seller_cpf)
        if not seller:
            return None
        
        sales = self.sale_repository.get_sales_by_seller(seller_cpf)
        return [self.to_dict(sale) for sale in sales]

    def get_summary_by_seller(self, seller_cpf):
        seller = self.seller_repository.get_seller_by_cpf(seller_cpf)
        if not seller:
            return None
        
        sales = self.get_sales_by_seller(seller_cpf)
        total_value = sum(sale['value'] for sale in sales)
        average_value = round(total_value / len(sales), 2) if sales else 0
        total_commission = sum(sale['commission'] for sale in sales)
        average_commission = round(total_commission / len(sales), 2) if sales else 0
        return {
            'seller_cpf': seller_cpf,
            'total_value': total_value,
            'average_value': average_value,
            'total_commission': total_commission,
            'average_commission': average_commission,
            'sales': sales
        }

    def to_dict(self, sale: Sale):
        return {
            'id': sale.id,
            'seller_cpf': sale.seller_cpf,
            'value': sale.value,
            'channel': sale.channel,
            'commission': sale.commission,
            'date': sale.date.strftime("%Y-%m-%d %H:%M:%S"),
            'client_type': sale.client_type,
            'currency': sale.currency
        }
