# 🚗 Car Rental API

## About the Project
This project is a backend system built using FastAPI as part of internship training. It simulates a real-world car rental service where users can view cars, book rentals, and manage returns.

The goal of this project was to apply concepts like API design, validation, workflows, and data handling in a real-world scenario.

---

## What This Project Does
- View all available cars
- Get details of a specific car
- Book a car for rental
- Calculate rental cost with discounts, insurance, and driver options
- Return a rented car
- Search, filter, and sort cars
- Pagination for large datasets
- View active rentals and rental history

---

## 🚀 Technologies Used
- Python  
- FastAPI  
- Pydantic  
- Uvicorn  

---

## 📁 Project Structure

project/
│── main.py
│── requirements.txt
│── README.md
└── screenshots/


---

## ▶️ How to Run the Project
1. Install dependencies:
```bash
pip install -r requirements.txt
Run the server:
uvicorn main:app --reload
Open Swagger UI in the browser:
http://127.0.0.1:8000/docs
📌 Key Features Implemented
✅ GET APIs for retrieving cars and rentals
✅ POST APIs with Pydantic validation for creating rentals and cars
✅ CRUD operations for cars (Create, Read, Update, Delete)
✅ Helper functions (find_car, calculate_rental_cost, filter_cars_logic)
✅ Multi-step workflow (Rent → Return)
✅ Rental cost calculation with:
Discounts for 7+ or 15+ days
Insurance charges
Driver charges
✅ Search, filter, and sort cars
✅ Pagination for cars and rentals
✅ Combined /cars/browse endpoint for advanced filtering, sorting, and pagination
📋 Sample Request Bodies

Add a New Car

{
  "model": "Sierra",
  "brand": "Tata",
  "type": "SUV",
  "price_per_day": 3500,
  "fuel_type": "Diesel",
  "is_available": true
}

Create a Rental

{
  "customer_name": "Ruchi",
  "car_id": 1,
  "days": 5,
  "license_number": "LIC12345",
  "insurance": true,
  "driver_required": false
}
📌 API Endpoints
Cars
GET /cars → Get all cars
GET /cars/{car_id} → Get car by ID
GET /cars/summary → Cars summary
GET /cars/filter → Filter cars
GET /cars/search → Search cars by keyword
GET /cars/sort → Sort cars
GET /cars/page → Paginate cars
GET /cars/unavailable → Get unavailable cars
GET /cars/browse → Combined search, filter, sort & pagination
POST /cars → Add new car
PUT /cars/{car_id} → Update car details
DELETE /cars/{car_id} → Delete car
Rentals
GET /rentals → Get all rentals
GET /rentals/active → Get active rentals
GET /rentals/{rental_id} → Get rental by ID
GET /rentals/by-car/{car_id} → Rental history by car
GET /rentals/search → Search rentals by customer name
GET /rentals/sort → Sort rentals by total cost or days
GET /rentals/page → Paginate rentals
POST /rentals → Create rental
POST /return/{rental_id} → Return rented car
🔑 Learning Outcome

Through this project, I learned how to:

Design structured APIs using FastAPI
Handle validations using Pydantic
Implement real-world rental workflows
Work with filtering, sorting, and pagination
Build a complete backend system from scratch
🙏 Acknowledgement

Built as part of the Advanced GenerativeAI Internship at Innomatics Research Labs.