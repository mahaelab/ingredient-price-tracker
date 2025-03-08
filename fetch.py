import os
import requests
import json
import csv

api_key = "5f95ae2543f48530e8f8a62dda035dc91d8b5dc6ad0b75195f304d5c853a76a8"  

ingredients = {
    "milk": f"https://serpapi.com/search.json?q=Horizon+Organic+Milk&engine=google_shopping&gl=us&hl=en&location=Orlando,Florida,United+States&api_key={api_key}",
    "eggs": f"https://serpapi.com/search.json?q=eggs&engine=google_shopping&gl=us&hl=en&location=Orlando,Florida,United+States&api_key={api_key}",
    "bread": f"https://serpapi.com/search.json?q=Sara+Lee+butter+bread&engine=google_shopping&gl=us&hl=en&location=Orlando,Florida,United+States&api_key={api_key}",
    "orange juice": f"https://serpapi.com/search.json?q=Simply+Orange+Juice&engine=google_shopping&gl=us&hl=en&location=Orlando,Florida,United+States&api_key={api_key}",
    "butter": f"https://serpapi.com/search.json?q=Land+O+Lakes+butter&engine=google_shopping&gl=us&hl=en&location=Orlando,Florida,United+States&api_key={api_key}"
}

allowed_stores = ["Walmart", "Target", "Sam's Club", "Publix"]

def fetch_grocery_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [
            {
                "title": item.get("title", "N/A"),
                "source": item.get("source", "N/A"),
                "price": item.get("extracted_price", "N/A")
            }
            for item in data.get("shopping_results", [])  
            if any(store in item.get("source", "") for store in allowed_stores)  
        ]
    else:
        print(f"Error fetching data: {response.status_code}, Response: {response.text}")
        return []

grocery_data = {}

for ingredient, url in ingredients.items():
    grocery_data[ingredient] = fetch_grocery_data(url)

json_filename = "grocery_prices.json"
with open(json_filename, "w") as json_file:
    json.dump(grocery_data, json_file, indent=4)

print(f"Data saved to {json_filename}")

csv_filename = "grocery_prices.csv"

with open(csv_filename, "w", newline="") as csv_file:
    fieldnames = ["ingredient", "title", "source", "price"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for ingredient, items in grocery_data.items():
        for item in items:
            writer.writerow({
                "ingredient": ingredient,
                "title": item["title"],
                "source": item["source"],
                "price": item["price"]
            })

print(f"Data saved to {csv_filename}")
