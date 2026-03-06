from fastapi import FastAPI
app = FastAPI()

products = [
    {'id' : 1, 'name' : 'Wireless Mouse', 'price': 499, 'category': 'Electronics', 'in_stock': True},
    {'id' : 2, 'name' : 'Notebook', 'price': 99, 'category': 'Stationery', 'in_stock': True},
    {'id' : 3, 'name' : 'USB Hub', 'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id' : 4, 'name' : 'Pen Set', 'price': 49, 'category': 'Stationery', 'in_stock': True},
    
    # Task 1: adding 3 new products
    {'id' : 5, 'name' : 'Laptop Stand', 'price': 1299, 'category': 'Electronics', 'in_stock': True},  
    {'id' : 6, 'name' : 'Mechanical Keyboard', 'price': 2499, 'category': 'Electronics', 'in_stock': True},
    {'id' : 7, 'name' : 'Webcam', 'price': 1899, 'category': 'Electronics', 'in_stock': False},
]

@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

# Task 1
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

# Task 2: adding a category filter endpoint
@app.get('/products/category/{category_name}')
def get_by_category(category_name:str):
    result = [p for p in products if p['category'] == category_name]
    if not result:
        return {'error': 'No products found in this category'}
    return {'category':category_name, 'products': result, 'total': len(result)}

# Task 3: Show Only In-Stock Products
@app.get('/products/instock')
def get_instock_products():
    instock_products = [product for product in products if product['in_stock'] == True]
    
    return {
        "in_stock_products": instock_products,
        "count": len(instock_products)
    }

# Task 4: Build a Store Info Endpoint
@app.get('/store/summary')
def store_summary():
    total_products = len(products)
    in_stock = len([p for p in products if p['in_stock']])
    out_of_stock = len([p for p in products if not p['in_stock']])
    categories = list(set([p['category'] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock,
        "out_of_stock": out_of_stock,
        "categories": categories
    }

# Task 5: Search Products by Name
@app.get('/products/search/{keyword}')
def search_products(keyword: str):
    matched_products = [
        product for product in products
        if keyword.lower() in product['name'].lower()
    ]

    if not matched_products:
        return {"message": "No products matched your search"}

    return {
        "matched_products": matched_products,
        "count": len(matched_products)
    }

# Task Bonus: Cheapest & Most Expensive Product
@app.get('/products/deals')
def get_product_deals():
    cheapest_product = min(products, key=lambda x: x['price'])
    most_expensive_product = max(products, key=lambda x: x['price'])

    return {
        "best_deal": cheapest_product,
        "premium_pick": most_expensive_product
    }
