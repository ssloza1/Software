# dao_product.py
import re
from datetime import datetime
from db import get_db

class ProductDAO:
    def __init__(self):
        self.col = get_db()["PRODUCT"]

    def generate_next_product_id(self) -> str:
        today = datetime.now().strftime("%Y%m%d")  # yyyyMMdd

        # buscar el último productId del día, ej: 20260106-003
        last = self.col.find(
            {"productId": {"$regex": f"^{today}-"}}, {"_id": 0, "productId": 1}
        ).sort("productId", -1).limit(1)

        last_doc = next(last, None)
        next_seq = 1

        if last_doc and "productId" in last_doc:
            m = re.match(rf"^{today}-(\d{{3}})$", last_doc["productId"])
            if m:
                next_seq = int(m.group(1)) + 1

        return f"{today}-{next_seq:03d}"

    def insert_product(self, product_id: str, name: str, detail: str, stock: int, price: float):
        doc = {
            "productId": product_id,
            "name": name,
            "detail": detail,
            "stock": stock,
            "price": price,
            "createdAt": datetime.utcnow().isoformat()
        }
        self.col.insert_one(doc)

    def find_by_product_id(self, product_id: str):
        return self.col.find_one({"productId": product_id}, {"_id": 0})

    def find_by_name(self, name: str):
        return self.col.find_one({"name": name}, {"_id": 0})
