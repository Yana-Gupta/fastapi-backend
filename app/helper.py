import requests
from fastapi import FastAPI

app = FastAPI()
API_KEY = "sb9ncl4Pr9z1yICJfCpMDtGbf0SjO2ktpEiGCErm"  # Replace with your actual API key

def get_food_nutrition(food_name: str):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    # Specify the parameters for the food search request
    params = {
        "query": food_name,
        "pageSize": 1,
        "api_key": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        # Check if any results were found
        if data["totalHits"] > 0:
            food_item = data["foods"][0]
            # return food_item
        
            nutrients = food_item["foodNutrients"]
            calories = next((n for n in nutrients if n["nutrientName"] == "Energy" and n["unitName"] == "KCAL"), None)

            if calories:
                return {"food_name": food_item["description"], "calories": calories["value"]}
            else:
                return {"food_name": food_item["description"], "calories": "N/A"}
        else:
            return {"food_name": food_name, "calories": "Not found"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def get_all_calorie_count(foods: list):
    total_calories = 0
    for food in foods:
        total_calories += food.calories
    return total_calories    

