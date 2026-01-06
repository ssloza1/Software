# dao_bill.py
from datetime import datetime
from db import get_db

class BillDAO:
    def __init__(self):
        self.col = get_db()["bill"]

    def insert_bill(self, client_data: dict, items: list, subtotal: float, iva: float, total_neto: float):
        bill_id = datetime.now().strftime("%Y%m%d%H%M%S")
        doc = {
            "billId": bill_id,
            "client": client_data,
            "items": items,
            "subtotal": subtotal,
            "iva": iva,
            "totalNeto": total_neto,
            "createdAt": datetime.utcnow().isoformat()
        }
        self.col.insert_one(doc)
        return bill_id
