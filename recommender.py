import datetime

# SMART REAL-WORLD FOOD DATABASE WITH TIME CONTEXT
# Expanded to ensure we have enough items to display Top 10 per category
REAL_FOODS = [
    # BREAKFAST (Morning)
    {"name": "Masala Dosa", "cals": 350, "tags": ["Rice", "Vegetables"], "time": ["Morning"]},
    {"name": "Egg Puffs", "cals": 250, "tags": ["Eggs", "Junk Food", "Wheat/Roti"], "time": ["Morning", "Evening"]},
    {"name": "Veg Sandwich", "cals": 220, "tags": ["Vegetables", "Junk Food", "Wheat/Roti"], "time": ["Morning", "Evening"]},
    {"name": "Appam & Egg Roast", "cals": 300, "tags": ["Rice", "Eggs"], "time": ["Morning"]},
    {"name": "Idli & Sambar", "cals": 200, "tags": ["Rice", "Vegetables"], "time": ["Morning"]},
    {"name": "Chicken Sausage Omelette", "cals": 280, "tags": ["Eggs", "Chicken/Meat", "Junk Food"], "time": ["Morning"]},
    {"name": "Oats Porridge with Fruits", "cals": 250, "tags": ["Wheat/Roti", "Vegetables", "Dairy"], "time": ["Morning"]},
    {"name": "Puttu & Kadala Curry", "cals": 350, "tags": ["Rice", "Vegetables"], "time": ["Morning"]},
    {"name": "Boiled Eggs (2) & Toast", "cals": 220, "tags": ["Eggs", "Wheat/Roti"], "time": ["Morning"]},
    {"name": "Milk & Cornflakes", "cals": 200, "tags": ["Dairy", "Wheat/Roti"], "time": ["Morning"]},
    
    # LUNCH (Afternoon)
    {"name": "Kerala Meals with Fish Fry", "cals": 600, "tags": ["Rice", "Fish", "Vegetables"], "time": ["Afternoon"]},
    {"name": "Chicken Biryani", "cals": 700, "tags": ["Rice", "Chicken/Meat"], "time": ["Afternoon"]},
    {"name": "Veg Fried Rice", "cals": 400, "tags": ["Rice", "Vegetables", "Junk Food"], "time": ["Afternoon", "Night"]},
    {"name": "Fish Curry Meals", "cals": 500, "tags": ["Rice", "Fish"], "time": ["Afternoon"]},
    {"name": "Chapati & Dal Curry", "cals": 350, "tags": ["Wheat/Roti", "Vegetables"], "time": ["Afternoon", "Night"]},
    {"name": "Grilled Chicken Salad", "cals": 250, "tags": ["Chicken/Meat", "Vegetables"], "time": ["Afternoon", "Night"]},
    {"name": "Beef Biryani", "cals": 750, "tags": ["Rice", "Chicken/Meat"], "time": ["Afternoon"]},
    {"name": "Egg Fried Rice", "cals": 450, "tags": ["Rice", "Eggs", "Junk Food"], "time": ["Afternoon", "Night"]},
    
    # EVENING SNACKS (Tea Time)
    {"name": "Pazham Pori", "cals": 200, "tags": ["Sweets", "Junk Food"], "time": ["Evening"]},
    {"name": "Chicken Roll", "cals": 300, "tags": ["Chicken/Meat", "Junk Food", "Wheat/Roti"], "time": ["Evening"]},
    {"name": "Meat Puffs", "cals": 280, "tags": ["Chicken/Meat", "Junk Food", "Wheat/Roti"], "time": ["Evening"]},
    {"name": "Black Tea & Biscuits", "cals": 100, "tags": ["Sweets", "Dairy", "Wheat/Roti"], "time": ["Evening", "Morning"]},
    {"name": "Veg Samosa (2 pcs)", "cals": 260, "tags": ["Vegetables", "Junk Food"], "time": ["Evening"]},
    {"name": "Coffee & Cake", "cals": 300, "tags": ["Dairy", "Sweets"], "time": ["Evening"]},
    {"name": "Boiled Eggs (2)", "cals": 140, "tags": ["Eggs"], "time": ["Evening", "Morning"]},
    
    # DINNER (Night)
    {"name": "Chapati & Chicken Curry", "cals": 400, "tags": ["Wheat/Roti", "Chicken/Meat"], "time": ["Night"]},
    {"name": "Porotta & Beef Roast", "cals": 650, "tags": ["Wheat/Roti", "Chicken/Meat", "Junk Food"], "time": ["Night"]},
    {"name": "Salad Bowl with Boiled Egg", "cals": 150, "tags": ["Vegetables", "Eggs"], "time": ["Night"]},
    {"name": "Paneer Butter Masala & Naan", "cals": 550, "tags": ["Dairy", "Wheat/Roti", "Vegetables"], "time": ["Night", "Afternoon"]},
    {"name": "Grilled Fish & Veggies", "cals": 300, "tags": ["Fish", "Vegetables"], "time": ["Night"]},
    {"name": "Wheat Dosa & Chutney", "cals": 250, "tags": ["Wheat/Roti", "Vegetables"], "time": ["Night", "Morning"]},
    {"name": "Chicken Soup", "cals": 180, "tags": ["Chicken/Meat", "Vegetables"], "time": ["Night"]},
    {"name": "Oats & Milk", "cals": 220, "tags": ["Wheat/Roti", "Dairy"], "time": ["Night", "Morning"]}
]

class FoodRecommender:
    def __init__(self):
        print("🍲 Advanced AI Food Recommender Initialized.")

    def get_recommendations(self, user_tags, current_hour, custom_learned_foods=None):
        if custom_learned_foods is None:
            custom_learned_foods = []
            
        # 1. Determine Time Context (Morning, Afternoon, Evening, Night)
        if 5 <= current_hour < 11:
            time_context = "Morning"
        elif 11 <= current_hour < 16:
            time_context = "Afternoon"
        elif 16 <= current_hour < 19:
            time_context = "Evening"
        else:
            time_context = "Night"

        # 2. Combine base dataset with user's specifically learned custom foods
        full_dataset = REAL_FOODS + custom_learned_foods

        scored_foods = []
        seen_names = set() # To avoid duplicates in the dropdown

        # Convert user tags to a set for faster and accurate matching
        user_tags_set = set(user_tags)

        for food in full_dataset:
            food_name_lower = food["name"].lower()
            
            # Prevent duplicate entries
            if food_name_lower in seen_names:
                continue

            # 3. Filter by Time Context
            if time_context in food["time"]:
                # 4. Calculate Match Score based on combination intersections
                food_tags_set = set(food.get("tags", []))
                matches = food_tags_set.intersection(user_tags_set)
                score = len(matches)
                
                # Slight penalty for junk food if user didn't explicitly select it
                if "Junk Food" in food_tags_set and "Junk Food" not in user_tags_set:
                    score -= 1 
                    
                # Boost score heavily if this is a custom food the user explicitly learned/added
                if food in custom_learned_foods:
                    score += 2 

                # Only suggest if there is relevance (score > 0) OR it's a learned custom food
                if score > 0 or food in custom_learned_foods:
                    scored_foods.append({
                        "name": food["name"],
                        "cals": food["cals"],
                        "score": score
                    })
                    seen_names.add(food_name_lower)
        
        # 5. Sort by score (Highest match first)
        scored_foods = sorted(scored_foods, key=lambda x: x["score"], reverse=True)
        
        # 6. Strictly return Top 10 items
        result = [{"name": f['name'], "cals": f['cals']} for f in scored_foods[:10]]
        
        # 7. Fallback if no matches found at all
        if not result:
            result = [{"name": "Standard Balanced Meal", "cals": 500}]
            
        return result