from fastapi import FastAPI, Query, Response, status, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# ══ PYDANTIC MODELS ═══════════════════════════════════════════════

class NewProduct(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    in_stock: bool = True

# ══ DATA ══════════════════════════════════════════════════════════

products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics', 'in_stock': True},
    {'id': 2, 'name': 'Notebook', 'price': 99, 'category': 'Stationery', 'in_stock': True},
    {'id': 3, 'name': 'USB Hub', 'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set', 'price': 49, 'category': 'Stationery', 'in_stock': True},
]

orders = []
order_counter = 1


# GET ALL PRODUCTS

@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}


# Q1: POST ADD PRODUCT

@app.post("/products", status_code=201)
def add_product(product: NewProduct, response: Response):

    for p in products:
        if p["name"].lower() == product.name.lower():
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"error": "Product with this name already exists"}
        
    new_id = max(p["id"] for p in products) + 1

    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "in_stock": product.in_stock
    }

    products.append(new_product)

    return {
        "message": "Product added",
        "product": new_product
    }


# Q5: INVENTORY AUDIT 

@app.get("/products/audit")
def audit_products():

    total_products = len(products)

    in_stock_items = [p for p in products if p["in_stock"]]
    out_of_stock = [p["name"] for p in products if not p["in_stock"]]

    in_stock_count = len(in_stock_items)

    total_stock_value = sum(p["price"] * 10 for p in in_stock_items)

    most_expensive = max(products, key=lambda x: x["price"])

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_names": out_of_stock,
        "total_stock_value": total_stock_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }


# BONUS: CATEGORY DISCOUNT

@app.put("/products/discount")
def category_discount(category: str, discount_percent: int):

    updated_products = []

    for p in products:
        if p["category"].lower() == category.lower():
            new_price = int(p["price"] * (1 - discount_percent / 100))
            p["price"] = new_price
            updated_products.append({
                "name": p["name"],
                "new_price": new_price
            })

    if not updated_products:
        return {"message": "No products found in this category"}

    return {
        "updated_count": len(updated_products),
        "products": updated_products
    }


# Q4: GET PRODUCT BY ID

@app.get("/products/{product_id}")
def get_product(product_id: int):

    for p in products:
        if p["id"] == product_id:
            return p

    return {"error": "Product not found"}


# Q2: UPDATE PRODUCT

@app.put("/products/{product_id}")
def update_product(product_id: int,
                   price: int = Query(None, gt=0),
                   in_stock: bool = Query(None)):

    for p in products:
        if p["id"] == product_id:

            if price is not None:
                p["price"] = price

            if in_stock is not None:
                p["in_stock"] = in_stock

            return {"message": "Product updated", "product": p}

    raise HTTPException(status_code=404, detail="Product not found")


# Q3: DELETE PRODUCT

@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for i, p in enumerate(products):
        if p["id"] == product_id:
            deleted_name = p["name"]
            products.pop(i)
            return {"message": f"Product '{deleted_name}' deleted"}

    raise HTTPException(status_code=404, detail="Product not found")
