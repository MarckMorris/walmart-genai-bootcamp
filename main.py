# main.py

from fastapi import FastAPI, HTTPException
from typing import Dict
import asyncio

app = FastAPI(
    title="Walmart Product API",
    description="A simple API for retrieving product details."
)

class Product:
    def __init__(self, product_id: str, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price

    async def get_details(self) -> Dict:
        print(f"Fetching details for product {self.product_id}...")
        await asyncio.sleep(0.5)
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "status": "Available"
        }

mock_db = {
    "12345": Product(product_id="12345", name="Lego Set", price=49.99),
    "67890": Product(product_id="67890", name="Echo Dot", price=39.99),
}

@app.get("/product/{product_id}", response_model=Dict)
async def get_product(product_id: str):
    product = mock_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    details = await product.get_details()
    return details

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
