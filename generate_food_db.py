import pandas as pd
import random

print("⚙️ Generating Global Mega Food Database...")

# Base ingredients for combinatorial logic
bases = ["Rice", "Wheat/Roti", "Quinoa", "Pasta", "Noodles"]
proteins = ["Chicken/Meat", "Fish", "Eggs", "Tofu", "Lentils"]
veg_types = ["Vegetables", "Leafy Greens", "Root Veggies", "Mixed Salad"]
extras = ["Dairy", "Nuts", "Sweets", "Junk Food"]

data = []

# Generate 2000+ realistic food combinations
for i in range(2000):
    meal_tags = []
    meal_name_parts = []
    calories = 0
    
    # Randomly pick combination length
    combo_size = random.randint(1, 4)
    
    if combo_size >= 1:
        base = random.choice(bases)
        meal_tags.append(base)
        meal_name_parts.append(base)
        calories += random.randint(150, 300)
        
    if combo_size >= 2:
        protein = random.choice(proteins)
        meal_tags.append(protein)
        meal_name_parts.append(protein)
        calories += random.randint(100, 350)
        
    if combo_size >= 3:
        veg = random.choice(veg_types)
        meal_tags.append("Vegetables") # Normalize tag
        meal_name_parts.append(veg)
        calories += random.randint(50, 150)
        
    if combo_size == 4:
        extra = random.choice(extras)
        meal_tags.append(extra)
        if extra == "Dairy":
            meal_name_parts.append("with Cheese/Cream")
            calories += 100
        elif extra == "Junk Food":
            meal_name_parts.append("(Fried/Processed)")
            calories += 300
    
    # Construct Meal Name (e.g., "Rice and Chicken/Meat and Vegetables")
    meal_name = " + ".join(meal_name_parts) + f" Combo {i+1}"
    
    # Create the tags string for the AI to read
    tag_string = " ".join(meal_tags)
    
    data.append({
        "Meal_Name": meal_name,
        "Calories": calories,
        "Tags": tag_string
    })

# Add some specific global items manually to ensure variety
manual_items = [
    {"Meal_Name": "Classic Beef Burger with Fries", "Calories": 850, "Tags": "Junk Food Chicken/Meat Wheat/Roti"},
    {"Meal_Name": "Grilled Salmon Salad", "Calories": 320, "Tags": "Fish Vegetables"},
    {"Meal_Name": "Paneer Tikka Masala with Naan", "Calories": 550, "Tags": "Dairy Wheat/Roti Vegetables"},
    {"Meal_Name": "Vegan Buddha Bowl", "Calories": 400, "Tags": "Vegetables Rice"},
    {"Meal_Name": "Chocolate Fudge Brownie", "Calories": 450, "Tags": "Sweets Dairy Wheat/Roti"}
]
data.extend(manual_items)

df = pd.DataFrame(data)
df.to_csv("food_database.csv", index=False)
print("✅ Created 'food_database.csv' with 2000+ combinations!")