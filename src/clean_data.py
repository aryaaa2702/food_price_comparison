import json
import os
import pandas as pd


# ---------- Helper function: Deep search for "restaurants" ----------
def find_restaurants(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "restaurants":
                return value
            result = find_restaurants(value)
            if result is not None:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_restaurants(item)
            if result is not None:
                return result
    return None


# ---------- Main cleaning function ----------
def clean_city(raw_path, city_name):

    # Load raw JSON
    with open(raw_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    # Find restaurant list
    restaurants = find_restaurants(raw)
    if restaurants is None:
        raise ValueError(f"Restaurants not found in {raw_path}")

    cleaned_data = []

    # Extract required fields
    for r in restaurants:
        info = r.get("info", {})

        # Clean costForTwo → numeric
        cost = info.get("costForTwo")
        if cost:
            try:
                cost_numeric = int(
                    cost.replace("₹", "").replace(" for two", "").strip()
                )
            except:
                cost_numeric = None
        else:
            cost_numeric = None

        cleaned_data.append({
            "name": info.get("name"),
            "area": info.get("areaName"),
            "rating": info.get("avgRating"),
            "costForTwo": cost_numeric,
            "cuisines": ", ".join(info.get("cuisines", [])),
            "veg": info.get("veg"),
        })

    # Convert to DataFrame
    df = pd.DataFrame(cleaned_data)

    # Add city column
    df["city"] = city_name

    return df


# ---------- Run cleaning for multiple cities ----------
if __name__ == "__main__":

    df_delhi = clean_city(
        os.path.join("data", "raw", "delhi_raw.json"),
        "Delhi"
    )

    df_mumbai = clean_city(
        os.path.join("data", "raw", "mumbai_raw.json"),
        "Mumbai"
    )

    # Combine all cities
    df_all = pd.concat([df_delhi, df_mumbai], ignore_index=True)

    # Save final CSV
    OUTPUT_PATH = os.path.join("data", "processed", "restaurants_all_cities.csv")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    df_all.to_csv(OUTPUT_PATH, index=False)

    print("Combined dataset saved:", OUTPUT_PATH)
    print("\nRestaurant count by city:")
    print(df_all["city"].value_counts())
