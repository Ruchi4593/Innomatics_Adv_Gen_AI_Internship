from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(title="Car Rentals")


# -----------------------------
# Q1: Root endpoint
# -----------------------------
@app.get("/")
def home():
    return {"message": "Welcome to Car Rentals"}


# -----------------------------
# Q2: Initial cars data
# -----------------------------
cars = [
    {
        "id": 1,
        "model": "Swift",
        "brand": "Maruti",
        "type": "Hatchback",
        "price_per_day": 1800,
        "fuel_type": "Petrol",
        "is_available": True
    },
    {
        "id": 2,
        "model": "City",
        "brand": "Honda",
        "type": "Sedan",
        "price_per_day": 2800,
        "fuel_type": "Petrol",
        "is_available": True
    },
    {
        "id": 3,
        "model": "Creta",
        "brand": "Hyundai",
        "type": "SUV",
        "price_per_day": 3500,
        "fuel_type": "Diesel",
        "is_available": True
    },
    {
        "id": 4,
        "model": "Nexon EV",
        "brand": "Tata",
        "type": "SUV",
        "price_per_day": 4000,
        "fuel_type": "Electric",
        "is_available": True
    },
    {
        "id": 5,
        "model": "Verna",
        "brand": "Hyundai",
        "type": "Sedan",
        "price_per_day": 3000,
        "fuel_type": "Petrol",
        "is_available": False
    },
    {
        "id": 6,
        "model": "Fortuner",
        "brand": "Toyota",
        "type": "Luxury",
        "price_per_day": 6500,
        "fuel_type": "Diesel",
        "is_available": True
    }
]

rentals = []
rental_counter = 1


# -----------------------------
# Q6 & Q9: Pydantic models
# -----------------------------
class RentalRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    car_id: int = Field(..., gt=0)
    days: int = Field(..., gt=0, le=30)
    license_number: str = Field(..., min_length=8)
    insurance: bool = False
    driver_required: bool = False


class NewCar(BaseModel):
    model: str = Field(..., min_length=2)
    brand: str = Field(..., min_length=2)
    type: str = Field(..., min_length=2)
    price_per_day: int = Field(..., gt=0)
    fuel_type: str = Field(..., min_length=2)
    is_available: bool = True


# -----------------------------
# Q7: Helper functions
# -----------------------------
def find_car(car_id: int):
    for car in cars:
        if car["id"] == car_id:
            return car
    return None


def find_rental(rental_id: int):
    for rental in rentals:
        if rental["rental_id"] == rental_id:
            return rental
    return None


def calculate_rental_cost(price_per_day: int, days: int, insurance: bool, driver_required: bool):
    base_cost = price_per_day * days

    discount_rate = 0
    if days >= 15:
        discount_rate = 0.25
    elif days >= 7:
        discount_rate = 0.15

    discount = int(base_cost * discount_rate)
    insurance_cost = 500 * days if insurance else 0
    driver_cost = 800 * days if driver_required else 0
    total_cost = base_cost - discount + insurance_cost + driver_cost

    return {
        "base_cost": base_cost,
        "discount": discount,
        "insurance_cost": insurance_cost,
        "driver_cost": driver_cost,
        "total_cost": total_cost
    }


def filter_cars_logic(
    type: Optional[str] = None,
    brand: Optional[str] = None,
    fuel_type: Optional[str] = None,
    max_price: Optional[int] = None,
    is_available: Optional[bool] = None
):
    filtered = cars

    if type is not None:
        filtered = [car for car in filtered if car["type"].lower() == type.lower()]

    if brand is not None:
        filtered = [car for car in filtered if car["brand"].lower() == brand.lower()]

    if fuel_type is not None:
        filtered = [car for car in filtered if car["fuel_type"].lower() == fuel_type.lower()]

    if max_price is not None:
        filtered = [car for car in filtered if car["price_per_day"] <= max_price]

    if is_available is not None:
        filtered = [car for car in filtered if car["is_available"] == is_available]

    return filtered


# -----------------------------
# Q5: Cars summary
# Keep fixed routes above /cars/{car_id}
# -----------------------------
@app.get("/cars/summary")
def cars_summary():
    total_cars = len(cars)
    available_count = sum(1 for car in cars if car["is_available"])

    breakdown_by_type = {}
    breakdown_by_fuel_type = {}

    for car in cars:
        breakdown_by_type[car["type"]] = breakdown_by_type.get(car["type"], 0) + 1
        breakdown_by_fuel_type[car["fuel_type"]] = breakdown_by_fuel_type.get(car["fuel_type"], 0) + 1

    cheapest_car = min(cars, key=lambda x: x["price_per_day"]) if cars else None
    most_expensive_car = max(cars, key=lambda x: x["price_per_day"]) if cars else None

    return {
        "total_cars": total_cars,
        "available_count": available_count,
        "breakdown_by_type": breakdown_by_type,
        "breakdown_by_fuel_type": breakdown_by_fuel_type,
        "cheapest_car_per_day": cheapest_car,
        "most_expensive_car_per_day": most_expensive_car
    }


# -----------------------------
# Q10: Filter cars
# -----------------------------
@app.get("/cars/filter")
def filter_cars(
    type: Optional[str] = None,
    brand: Optional[str] = None,
    fuel_type: Optional[str] = None,
    max_price: Optional[int] = None,
    is_available: Optional[bool] = None
):
    filtered = filter_cars_logic(type, brand, fuel_type, max_price, is_available)
    return {
        "cars": filtered,
        "total": len(filtered)
    }


# -----------------------------
# Q16: Search cars
# -----------------------------
@app.get("/cars/search")
def search_cars(keyword: str = Query(..., min_length=1)):
    keyword_lower = keyword.lower()
    matched = [
        car for car in cars
        if keyword_lower in car["model"].lower()
        or keyword_lower in car["brand"].lower()
        or keyword_lower in car["type"].lower()
    ]
    return {
        "keyword": keyword,
        "matches": matched,
        "total_found": len(matched)
    }


# -----------------------------
# Q17: Sort cars
# -----------------------------
@app.get("/cars/sort")
def sort_cars(
    sort_by: str = Query("price_per_day", pattern="^(price_per_day|brand|type)$"),
    order: str = Query("asc", pattern="^(asc|desc)$")
):
    reverse = order == "desc"
    sorted_cars = sorted(cars, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "cars": sorted_cars
    }


# -----------------------------
# Q18: Paginate cars
# -----------------------------
@app.get("/cars/page")
def paginate_cars(
    page: int = Query(1, gt=0),
    limit: int = Query(3, gt=0)
):
    total = len(cars)
    start = (page - 1) * limit
    end = start + limit
    paginated = cars[start:end]

    if start >= total and total > 0:
        raise HTTPException(status_code=404, detail="Page not found")

    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "cars": paginated
    }


# -----------------------------
# Q15: Unavailable cars
# -----------------------------
@app.get("/cars/unavailable")
def get_unavailable_cars():
    unavailable = [car for car in cars if not car["is_available"]]
    return {
        "cars": unavailable,
        "total": len(unavailable)
    }


# -----------------------------
# Q20: Browse cars
# -----------------------------
@app.get("/cars/browse")
def browse_cars(
    keyword: Optional[str] = None,
    type: Optional[str] = None,
    fuel_type: Optional[str] = None,
    max_price: Optional[int] = None,
    is_available: Optional[bool] = None,
    sort_by: str = Query("price_per_day", pattern="^(price_per_day|brand|type)$"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    page: int = Query(1, gt=0),
    limit: int = Query(3, gt=0)
):
    results = cars

    if keyword is not None:
        keyword_lower = keyword.lower()
        results = [
            car for car in results
            if keyword_lower in car["model"].lower()
            or keyword_lower in car["brand"].lower()
            or keyword_lower in car["type"].lower()
        ]

    if type is not None:
        results = [car for car in results if car["type"].lower() == type.lower()]

    if fuel_type is not None:
        results = [car for car in results if car["fuel_type"].lower() == fuel_type.lower()]

    if max_price is not None:
        results = [car for car in results if car["price_per_day"] <= max_price]

    if is_available is not None:
        results = [car for car in results if car["is_available"] == is_available]

    reverse = order == "desc"
    results = sorted(results, key=lambda x: x[sort_by], reverse=reverse)

    total_results = len(results)
    total_pages = (total_results + limit - 1) // limit if total_results > 0 else 0
    start = (page - 1) * limit
    end = start + limit
    paginated_results = results[start:end]

    if start >= total_results and total_results > 0:
        raise HTTPException(status_code=404, detail="Page not found")

    return {
        "filters": {
            "keyword": keyword,
            "type": type,
            "fuel_type": fuel_type,
            "max_price": max_price,
            "is_available": is_available,
            "sort_by": sort_by,
            "order": order,
            "page": page,
            "limit": limit
        },
        "total_results": total_results,
        "total_pages": total_pages,
        "results": paginated_results
    }


# -----------------------------
# Q2: Get all cars
# -----------------------------
@app.get("/cars")
def get_cars():
    available_count = sum(1 for car in cars if car["is_available"])
    return {
        "cars": cars,
        "total": len(cars),
        "available_count": available_count
    }


# -----------------------------
# Q3: Get car by ID
# -----------------------------
@app.get("/cars/{car_id}")
def get_car(car_id: int):
    car = find_car(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


# -----------------------------
# Q4: Get all rentals
# -----------------------------
@app.get("/rentals")
def get_rentals():
    return {
        "rentals": rentals,
        "total": len(rentals)
    }


# -----------------------------
# Q15: Active rentals
# -----------------------------
@app.get("/rentals/active")
def get_active_rentals():
    active_rentals = [rental for rental in rentals if rental["status"] == "active"]
    return {
        "rentals": active_rentals,
        "total": len(active_rentals)
    }


# -----------------------------
# Q19: Search rentals
# -----------------------------
@app.get("/rentals/search")
def search_rentals(customer_name: str = Query(..., min_length=1)):
    keyword_lower = customer_name.lower()
    matched = [
        rental for rental in rentals
        if keyword_lower in rental["customer_name"].lower()
    ]
    return {
        "customer_name": customer_name,
        "matches": matched,
        "total_found": len(matched)
    }


# -----------------------------
# Q19: Sort rentals
# -----------------------------
@app.get("/rentals/sort")
def sort_rentals(
    sort_by: str = Query(..., pattern="^(total_cost|days)$"),
    order: str = Query("asc", pattern="^(asc|desc)$")
):
    reverse = order == "desc"
    sorted_rentals = sorted(rentals, key=lambda x: x[sort_by], reverse=reverse)
    return {
        "sort_by": sort_by,
        "order": order,
        "rentals": sorted_rentals
    }


# -----------------------------
# Q19: Paginate rentals
# -----------------------------
@app.get("/rentals/page")
def paginate_rentals(
    page: int = Query(1, gt=0),
    limit: int = Query(3, gt=0)
):
    total = len(rentals)
    start = (page - 1) * limit
    end = start + limit
    paginated = rentals[start:end]

    if start >= total and total > 0:
        raise HTTPException(status_code=404, detail="Page not found")

    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "rentals": paginated
    }


# -----------------------------
# Q14: Get rental by ID
# -----------------------------
@app.get("/rentals/{rental_id}")
def get_rental_by_id(rental_id: int):
    rental = find_rental(rental_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental


# -----------------------------
# Q15: Rental history by car
# -----------------------------
@app.get("/rentals/by-car/{car_id}")
def rentals_by_car(car_id: int):
    car = find_car(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    car_rentals = [rental for rental in rentals if rental["car_id"] == car_id]
    return {
        "car_id": car_id,
        "car_model": car["model"],
        "rental_history": car_rentals,
        "total": len(car_rentals)
    }


# -----------------------------
# Q8 & Q9: Create rental
# -----------------------------
@app.post("/rentals", status_code=status.HTTP_201_CREATED)
def create_rental(request: RentalRequest):
    global rental_counter

    car = find_car(request.car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    if not car["is_available"]:
        raise HTTPException(status_code=400, detail="Car is not available")

    cost_details = calculate_rental_cost(
        price_per_day=car["price_per_day"],
        days=request.days,
        insurance=request.insurance,
        driver_required=request.driver_required
    )

    rental = {
        "rental_id": rental_counter,
        "customer_name": request.customer_name,
        "car_id": request.car_id,
        "car_model": car["model"],
        "car_brand": car["brand"],
        "days": request.days,
        "license_number": request.license_number,
        "insurance": request.insurance,
        "driver_required": request.driver_required,
        "base_cost": cost_details["base_cost"],
        "discount": cost_details["discount"],
        "insurance_cost": cost_details["insurance_cost"],
        "driver_cost": cost_details["driver_cost"],
        "total_cost": cost_details["total_cost"],
        "status": "active"
    }

    rentals.append(rental)
    rental_counter += 1
    car["is_available"] = False

    return {
        "message": "Rental created successfully",
        "rental": rental
    }


# -----------------------------
# Q11: Add new car
# -----------------------------
@app.post("/cars", status_code=status.HTTP_201_CREATED)
def add_car(new_car: NewCar):
    for car in cars:
        if car["model"].lower() == new_car.model.lower() and car["brand"].lower() == new_car.brand.lower():
            raise HTTPException(status_code=400, detail="Car with this model and brand already exists")

    new_id = max([car["id"] for car in cars], default=0) + 1

    car_data = {
        "id": new_id,
        "model": new_car.model,
        "brand": new_car.brand,
        "type": new_car.type,
        "price_per_day": new_car.price_per_day,
        "fuel_type": new_car.fuel_type,
        "is_available": new_car.is_available
    }

    cars.append(car_data)
    return {
        "message": "Car added successfully",
        "car": car_data
    }


# -----------------------------
# Q12: Update car
# -----------------------------
@app.put("/cars/{car_id}")
def update_car(
    car_id: int,
    price_per_day: Optional[int] = Query(None, gt=0),
    is_available: Optional[bool] = None
):
    car = find_car(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    if price_per_day is not None:
        car["price_per_day"] = price_per_day

    if is_available is not None:
        car["is_available"] = is_available

    return {
        "message": "Car updated successfully",
        "car": car
    }


# -----------------------------
# Q13: Delete car
# -----------------------------
@app.delete("/cars/{car_id}")
def delete_car(car_id: int):
    car = find_car(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    active_rental = next(
        (rental for rental in rentals if rental["car_id"] == car_id and rental["status"] == "active"),
        None
    )
    if active_rental:
        raise HTTPException(status_code=400, detail="Cannot delete car with an active rental")

    cars.remove(car)
    return {
        "message": "Car deleted successfully",
        "deleted_car": car
    }


# -----------------------------
# Q14: Return rental workflow
# -----------------------------
@app.post("/return/{rental_id}")
def return_rental(rental_id: int):
    rental = find_rental(rental_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")

    if rental["status"] == "returned":
        raise HTTPException(status_code=400, detail="Rental already returned")

    rental["status"] = "returned"

    car = find_car(rental["car_id"])
    if car:
        car["is_available"] = True

    return {
        "message": "Car returned successfully",
        "rental": rental
    }
