#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- 1. Setup Virtual Environment and Dependencies ---
echo "--- Setting up virtual environment and installing dependencies... ---"
python -m venv .venv
# Use 'source' for Linux/WSL, but MINGW64 can handle it as well
source .venv/Scripts/activate

# Install core dependencies with the correct version for our Docker image (Python 3.11)
pip install "fastapi[all]" uvicorn==0.23.2 black==23.7.0 ruff==0.0.280

# Generate a clean requirements.txt for Docker
pip freeze > requirements.txt

# Create a .dockerignore file to prevent conflicts
echo ".venv/" > .dockerignore
echo "__pycache__/" >> .dockerignore

# --- 2. Create the FastAPI Application File ---
echo "--- Creating main.py for the FastAPI application... ---"
cat > main.py << EOL
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
EOL

# --- 3. Create the Dockerfile ---
echo "--- Creating Dockerfile... ---"
cat > Dockerfile << EOL
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOL

# --- 4. Build and Run the Docker Container ---
echo "--- Building Docker image and running container... ---"
docker build -t walmart-product-api:latest .
docker run -p 8000:8000 walmart-product-api:latest

echo "--- Script finished. Your API should be running. Access at http://localhost:8000/docs ---"