from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import joblib
import re
import random 

from recommender import FoodRecommender

app = Flask(__name__)

# ==========================================
# 1. DATABASE & AI INITIALIZATION
# ==========================================
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["metabolic_ai_core"]
    users_collection = db["users"]
    logs_collection = db["daily_metrics"] 
    print("✅ Core API Engine successfully connected to MongoDB!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")

try:
    ai_model = joblib.load('ai_brain.pkl')
except Exception as e:
    ai_model = None

food_ai = FoodRecommender()

# ==========================================
# 2. ADVANCED EXERCISE DATABASE & ENGINE
# ==========================================
EXERCISE_DATABASE = [
    {"name": "Bodyweight Squats", "category": "Strength", "intensity": "Medium", "base_metrics": "3 Sets x 15 Reps", "desc": "Great for lower body strength. Keep your chest up and back straight."},
    {"name": "Push-Ups", "category": "Strength", "intensity": "High", "base_metrics": "3 Sets x 10 Reps", "desc": "Core upper body push mechanics. Drop to knees if form breaks."},
    {"name": "Lunges", "category": "Strength", "intensity": "Medium", "base_metrics": "3 Sets x 12 Reps (Each Leg)", "desc": "Improves balance and leg strength. Step forward and lower hips."},
    {"name": "Glute Bridges", "category": "Strength", "intensity": "Low", "base_metrics": "3 Sets x 15 Reps", "desc": "Activates the posterior chain. Squeeze glutes at the top."},
    {"name": "Wall Sit", "category": "Strength", "intensity": "Medium", "base_metrics": "3 Sets x 45 Sec Hold", "desc": "Isometric leg burn. Keep legs at exactly 90 degrees."},
    {"name": "Brisk Walk / Light Jog", "category": "Cardio", "intensity": "Low", "base_metrics": "20 Mins Steady", "desc": "Steady state cardiovascular exercise to burn fat efficiently."},
    {"name": "Jumping Jacks", "category": "Cardio", "intensity": "Medium", "base_metrics": "3 Sets x 60 Sec", "desc": "Full body warmup that elevates heart rate instantly."},
    {"name": "High Knees", "category": "Cardio", "intensity": "High", "base_metrics": "4 Sets x 30 Sec", "desc": "Explosive movement to trigger metabolic conditioning."},
    {"name": "Spot Running", "category": "Cardio", "intensity": "Medium", "base_metrics": "5 Mins Intervals", "desc": "Run in place. 30 seconds fast, 30 seconds slow."},
    {"name": "Plank Hold", "category": "Core", "intensity": "Medium", "base_metrics": "3 Sets x 45 Sec Hold", "desc": "Isometric core engagement to improve standard posture alignment."},
    {"name": "Russian Twists", "category": "Core", "intensity": "Medium", "base_metrics": "3 Sets x 20 Reps", "desc": "Targets obliques. Sit in a V-shape and twist torso."},
    {"name": "Bicycle Crunches", "category": "Core", "intensity": "High", "base_metrics": "3 Sets x 15 Reps (Each side)", "desc": "Intense abdominal engagement. Touch elbow to opposite knee."},
    {"name": "Leg Raises", "category": "Core", "intensity": "Medium", "base_metrics": "3 Sets x 12 Reps", "desc": "Targets lower abs. Keep legs straight and lower slowly."},
    {"name": "Burpees", "category": "HIIT", "intensity": "High", "base_metrics": "4 Sets x 10 Reps", "desc": "Ultimate full-body calorie incinerator."},
    {"name": "Mountain Climbers", "category": "HIIT", "intensity": "High", "base_metrics": "4 Sets x 45 Sec", "desc": "Rapid core and cardio fusion. Keep hips down."},
    {"name": "Jump Squats", "category": "HIIT", "intensity": "High", "base_metrics": "4 Sets x 12 Reps", "desc": "Explosive lower body power generation."},
    {"name": "Child's Pose Stretch", "category": "Recovery", "intensity": "Low", "base_metrics": "2 Mins Hold", "desc": "Restful pose to relax lower back and nervous system."},
    {"name": "Cat-Cow Yoga Flow", "category": "Recovery", "intensity": "Low", "base_metrics": "2 Mins Continuous", "desc": "Gentle spinal mobility to relieve tension."},
    {"name": "Cobra Stretch", "category": "Recovery", "intensity": "Low", "base_metrics": "3 Sets x 20 Sec Hold", "desc": "Opens up the chest and stretches abdominal muscles."},
    {"name": "Hamstring & Calf Stretch", "category": "Recovery", "intensity": "Low", "base_metrics": "2 Mins Hold", "desc": "Promotes blood flow to the legs without metabolic stress."}
]

# Helper Function to safely parse numbers
def extract_safe_number(val, default=0.0):
    try:
        num_str = re.sub(r'[^\d.]', '', str(val))
        return float(num_str) if num_str else default
    except:
        return default

# ACCURATE SCORING LOGIC
def calculate_health_score(age, weight_kg, height_cm, activity_level, liked_foods):
    score = 80.0 
    
    if height_cm > 0:
        bmi = weight_kg / ((height_cm / 100.0) ** 2)
        if 18.5 <= bmi <= 24.9:
            score += 15.0
        elif 25.0 <= bmi <= 29.9:
            score -= (bmi - 24.9) * 2.0
        elif bmi >= 30.0:
            score -= min(10.0 + (bmi - 30.0) * 1.5, 35.0)
        elif bmi < 18.5:
            score -= min((18.5 - bmi) * 2.5, 20.0)

    activity = str(activity_level).lower() if activity_level else ""
    if "sitting" in activity or "desk" in activity or "relax" in activity:
        score -= 12.0
    elif "light" in activity:
        score -= 4.0
    elif "moderate" in activity or "active" in activity:
        score += 8.0
    elif "heavy" in activity or "athlete" in activity:
        score += 15.0

    foods_str = str(liked_foods).lower()
    if "veggies" in foods_str or "vegetable" in foods_str: score += 5.0
    if "fish" in foods_str: score += 4.0
    if "eggs" in foods_str: score += 3.0
    if "meat" in foods_str or "chicken" in foods_str: score += 2.0
    if "dairy" in foods_str: score += 2.0
    
    if "fast food" in foods_str or "junk" in foods_str: score -= 12.0
    if "sweets" in foods_str or "sugar" in foods_str: score -= 10.0
    
    if ("rice" in foods_str or "wheat" in foods_str) and ("sitting" in activity or "desk" in activity):
        score -= 5.0

    if age > 30:
        score -= min((age - 30) * 0.3, 15.0)

    return int(max(10, min(100, round(score))))

# MODIFIED: Dynamically tracks scores in decimals for real-time adjustments
def adjust_user_health_score(username, amount):
    user = users_collection.find_one({"username": username})
    if user:
        current_score = float(user.get('health_score_100', 65.0))
        new_score = round(max(10.0, min(100.0, current_score + float(amount))), 1)
        status = "Optimal" if new_score >= 80 else "Good" if new_score >= 60 else "Moderate Risk" if new_score >= 40 else "High Risk"
        users_collection.update_one({"username": username}, {"$set": {"health_score_100": new_score, "health_status": status}})

def generate_adaptive_workout(user, calorie_target, water_target):
    username = user['username']
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_log = logs_collection.find_one({"username": username, "date": yesterday_date})
    
    y_cals = yesterday_log.get('calories_eaten', 0) if yesterday_log else 0
    y_sleep = yesterday_log.get('sleep_hours', 8) if yesterday_log else 8
    y_water = yesterday_log.get('water_drank_ml', water_target) if yesterday_log else water_target

    is_fatigued = (0 < y_sleep < 6)
    is_dehydrated = (0 < y_water < (water_target * 0.5))
    is_overfed = (y_cals > calorie_target)
    
    workout_plan = []
    
    if is_fatigued:
        pool = [ex for ex in EXERCISE_DATABASE if ex['category'] == 'Recovery' or ex['intensity'] == 'Low']
        selected = random.sample(pool, min(3, len(pool)))
    elif is_overfed:
        hiit_pool = [ex for ex in EXERCISE_DATABASE if ex['category'] == 'HIIT']
        cardio_pool = [ex for ex in EXERCISE_DATABASE if ex['category'] == 'Cardio' and ex['intensity'] == 'High']
        strength_pool = [ex for ex in EXERCISE_DATABASE if ex['category'] == 'Strength']
        hiit_choices = random.sample(hiit_pool, min(2, len(hiit_pool)))
        cardio_choices = random.sample(cardio_pool, min(1, len(cardio_pool))) if cardio_pool else []
        strength_choices = random.sample(strength_pool, 1)
        selected = hiit_choices + cardio_choices + strength_choices
    else:
        cardio = random.sample([ex for ex in EXERCISE_DATABASE if ex['category'] == 'Cardio'], 1)
        strength = random.sample([ex for ex in EXERCISE_DATABASE if ex['category'] == 'Strength'], 2)
        core = random.sample([ex for ex in EXERCISE_DATABASE if ex['category'] == 'Core'], 1)
        selected = cardio + strength + core

    for ex in selected:
        metrics = ex['base_metrics']
        if is_overfed and ex['category'] == 'Cardio':
            metrics = metrics.replace("20 Mins", "30 Mins").replace("5 Mins", "10 Mins")
        workout_plan.append({"name": ex['name'], "metrics": metrics, "desc": ex['desc']})

    return {"plan": workout_plan, "status_tags": {"fatigued": is_fatigued, "dehydrated": is_dehydrated, "overfed": is_overfed}}

def estimate_custom_calories(food_name):
    name_clean = food_name.lower()
    if "biryani" in name_clean: return 650
    elif "fried" in name_clean or "fry" in name_clean or "broast" in name_clean: return 450
    elif "burger" in name_clean or "pizza" in name_clean or "shawarma" in name_clean: return 600
    elif "puffs" in name_clean or "roll" in name_clean or "samosa" in name_clean: return 250
    elif "sandwich" in name_clean: return 220
    elif "roast" in name_clean or "curry" in name_clean or "masala" in name_clean:
        if "chicken" in name_clean or "beef" in name_clean or "meat" in name_clean: return 300
        if "fish" in name_clean: return 200
        return 150
    elif "egg" in name_clean or "omelette" in name_clean or "bulla" in name_clean: return 150
    elif "rice" in name_clean or "pulao" in name_clean: return 250
    elif "chapati" in name_clean or "roti" in name_clean or "porotta" in name_clean or "naan" in name_clean: return 140
    elif "dosa" in name_clean or "appam" in name_clean or "idli" in name_clean: return 120
    elif "salad" in name_clean: return 120
    elif "cake" in name_clean or "sweet" in name_clean or "payasam" in name_clean or "ice cream" in name_clean: return 350
    return 250 

def generate_daily_routine(y_cals, target_cals):
    routine = [
        {"id": "wake", "time": "06:00 AM", "title": "Wake Up & Fresh", "desc": "Start your day with positive energy.", "done": False},
        {"id": "water_morn", "time": "06:15 AM", "title": "Morning Hydration", "desc": "Drink 500ml water to kickstart metabolism.", "done": False},
        {"id": "workout_time", "time": "07:00 AM", "title": "AI Workout Circuit", "desc": "Check your personalized exercise options above.", "done": False},
        {"id": "meal_b", "time": "08:30 AM", "title": "Breakfast", "desc": "Healthy morning meal.", "done": False},
        {"id": "water_mid", "time": "11:00 AM", "title": "Mid-Morning Hydration", "desc": "Keep your body hydrated.", "done": False},
        {"id": "meal_l", "time": "01:30 PM", "title": "Lunch", "desc": "Balanced midday meal.", "done": False},
        {"id": "snack", "time": "04:30 PM", "title": "Tea & Light Snack", "desc": "Keep it light (e.g., Green tea & nuts).", "done": False},
        {"id": "water_eve", "time": "06:30 PM", "title": "Evening Hydration", "desc": "Drink water to process daily meals.", "done": False},
        {"id": "meal_d", "time": "08:00 PM", "title": "Dinner", "desc": "Light dinner for better overnight recovery.", "done": False}
    ]
    if y_cals > target_cals:
        routine.append({"id": "walk_eve", "time": "08:30 PM", "title": "Post-Dinner Walk", "desc": "15 min walk to aid digestion of excess calories.", "done": False})
    
    routine.append({"id": "sleep_setup", "time": "10:00 PM", "title": "Sleep Setup", "desc": "Log your sleep and prepare for rest.", "done": False})
    return routine

# ==========================================
# 3. PAGE ROUTES
# ==========================================
@app.route('/', methods=['GET'])
def home(): return render_template('index.html')
@app.route('/onboarding', methods=['GET'])
def onboarding(): return render_template('onboarding.html')
@app.route('/masterplan', methods=['GET'])
def masterplan(): return render_template('masterplan.html')
@app.route('/dashboard', methods=['GET'])
def dashboard(): return render_template('dashboard.html')
@app.route('/analytics', methods=['GET'])
def analytics(): return render_template('analytics.html')

# ==========================================
# 4. AUTHENTICATION & ONBOARDING
# ==========================================
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if users_collection.find_one({"username": username}): return jsonify({"status": "error", "message": "Username already exists."}), 400
    users_collection.insert_one({"username": username, "password": generate_password_hash(password), "profile_completed": False})
    return jsonify({"status": "success", "message": "Account created successfully!", "redirect": "/onboarding"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users_collection.find_one({"username": data.get('username')})
    if user and check_password_hash(user['password'], data.get('password')):
        return jsonify({"status": "success", "message": "Login successful!", "redirect": "/dashboard" if user.get("profile_completed") else "/onboarding"}), 200
    return jsonify({"status": "error", "message": "Invalid credentials."}), 401

@app.route('/api/onboard', methods=['POST'])
def onboard_user():
    data = request.get_json()
    username = data.get('username')
    
    height_cm = extract_safe_number(data.get('height'), 170.0)
    weight_kg = extract_safe_number(data.get('weight'), 70.0)
    age = int(extract_safe_number(data.get('age'), 25.0))
    
    if 0 < height_cm < 3.0: height_cm *= 100.0

    bmi = round(weight_kg / ((height_cm / 100) ** 2), 1) if height_cm > 0 else 0
    activity = data.get('activity', '')
    foods = data.get('foods', [])

    total_score = calculate_health_score(age, weight_kg, height_cm, activity, foods)

    status = "Optimal" if total_score >= 80 else "Good" if total_score >= 60 else "Moderate Risk" if total_score >= 40 else "High Risk"
    
    users_collection.update_one({"username": username}, {"$set": {
        "age": age, "weight_kg": weight_kg, "height_cm": height_cm, "usual_foods": foods, "daily_activity": activity,
        "baseline_bmi": bmi, "health_score_100": total_score, "health_status": status, "profile_completed": True, "custom_learned_foods": [] 
    }})
    
    return jsonify({"status": "success", "score": total_score, "health_status": status, "redirect": "/masterplan"}), 201

@app.route('/api/profile', methods=['POST'])
def get_profile():
    username = request.get_json().get('username')
    user = users_collection.find_one({"username": username})
    if user:
        display_score = int(round(float(user.get('health_score_100', 0))))
        return jsonify({"status": "success", "score": display_score, "health_status": user.get('health_status', 'Unknown')}), 200
    return jsonify({"status": "error"}), 404

# ==========================================
# 5. DASHBOARD DATA API
# ==========================================
@app.route('/api/dashboard_data', methods=['POST'])
def get_dashboard():
    username = request.get_json().get('username')
    user = users_collection.find_one({"username": username})
    if not user: return jsonify({"status": "error"}), 404

    water_target = int(user['weight_kg'] * 35) + (500 if user.get('daily_activity') in ['Moderate', 'Heavy'] else 0)
    calorie_target = int(10 * user['weight_kg'] + 6.25 * user['height_cm'] - 5 * user['age'])
    
    activity_steps = {"Sitting": 5000, "Light": 7500, "Moderate": 10000, "Heavy": 12000}
    
    act_str = str(user.get('daily_activity', '')).lower()
    dynamic_step_target = 5000
    if "light" in act_str: dynamic_step_target = 7500
    elif "moderate" in act_str: dynamic_step_target = 10000
    elif "heavy" in act_str: dynamic_step_target = 12000
    
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_log = logs_collection.find_one({"username": username, "date": yesterday_date})
    y_cals = yesterday_log.get('calories_eaten', 0) if yesterday_log else 0

    if yesterday_log:
        if y_cals > calorie_target: dynamic_step_target += int(((y_cals - calorie_target) / 10) * 25)
        if 0 < yesterday_log.get('sleep_hours', 0) < 6: dynamic_step_target = int(dynamic_step_target * 0.85)
        if 0 < yesterday_log.get('water_drank_ml', 0) < (water_target * 0.5): dynamic_step_target = int(dynamic_step_target * 0.90)

    current_hour = datetime.now().hour
    time_context = "Morning" if 5<=current_hour<11 else "Afternoon" if 11<=current_hour<16 else "Evening" if 16<=current_hour<19 else "Night"
    recommended_foods = food_ai.get_recommendations(user.get('usual_foods', []), current_hour, user.get('custom_learned_foods', []))

    today = datetime.now().strftime("%Y-%m-%d")
    log = logs_collection.find_one({"username": username, "date": today})
    
    expected_routine = generate_daily_routine(y_cals, calorie_target)
    
    if not log:
        locked_workout_plan = generate_adaptive_workout(user, calorie_target, water_target)
        log = {
            "username": username, "date": today, "water_drank_ml": 0, "calories_eaten": 0, "sleep_hours": 0, "steps": 0, 
            "foods_logged": [], "routine": expected_routine, "workouts_logged": [],
            "daily_locked_workout": locked_workout_plan,
            "rewards_tracked": {"water": False, "workout": False, "sleep": False, "calorie_penalty": False}
        }
        logs_collection.insert_one(log)
    else:
        updates = {}
        current_routine = log.get('routine', [])
        if len(current_routine) < len(expected_routine):
            done_map = {r.get('id'): r.get('done', False) for r in current_routine}
            for task in expected_routine:
                old_id = task['id']
                if old_id == 'workout_time' and 'workout_m' in done_map: old_id = 'workout_m'
                task['done'] = done_map.get(old_id, False)
            updates["routine"] = expected_routine
            log['routine'] = expected_routine

        if "daily_locked_workout" not in log:
            locked_workout_plan = generate_adaptive_workout(user, calorie_target, water_target)
            updates["daily_locked_workout"] = locked_workout_plan
            log["daily_locked_workout"] = locked_workout_plan
            
        if "rewards_tracked" not in log:
            updates["rewards_tracked"] = {"water": False, "workout": False, "sleep": False, "calorie_penalty": False}
            log["rewards_tracked"] = {"water": False, "workout": False, "sleep": False, "calorie_penalty": False}
            
        if updates:
            logs_collection.update_one({"_id": log["_id"]}, {"$set": updates})

    display_score = int(round(float(user.get('health_score_100', 0))))
    return jsonify({
        "status": "success", "score": f"{display_score}/100", 
        "time_context": time_context, 
        "workout_payload": log["daily_locked_workout"], 
        "targets": {"water_ml": water_target, "calories": calorie_target, "sleep_hrs": 8, "steps": round(max(4000, min(15000, dynamic_step_target))/100)*100},
        "current": {"water_ml": log.get('water_drank_ml', 0), "calories": log.get('calories_eaten', 0), "sleep_hrs": log.get('sleep_hours', 0), "steps": log.get('steps', 0), "foods": log.get('foods_logged', []), "routine": log.get('routine', []), "workouts": log.get('workouts_logged', [])},
        "recommendations": recommended_foods
    }), 200

# ==========================================
# 6. ACTION LOGGING ENGINE (REAL-TIME TRACKING ADDED)
# ==========================================
@app.route('/api/log_action', methods=['POST'])
def log_action():
    data = request.get_json()
    username = data.get('username')
    action_type = data.get('type') 
    value = data.get('value')
    today = datetime.now().strftime("%Y-%m-%d")
    hour = datetime.now().hour
    
    user = users_collection.find_one({"username": username})
    if not user: return jsonify({"status": "error"}), 404
    
    if action_type == 'water':
        amt = int(value)
        logs_collection.update_one({"username": username, "date": today}, {"$inc": {"water_drank_ml": amt}})
        r_id = "water_morn" if hour < 10 else "water_mid" if hour < 14 else "water_eve"
        is_done = True if amt > 0 else False
        logs_collection.update_one({"username": username, "date": today, "routine.id": r_id}, {"$set": {"routine.$.done": is_done}})
        
        if amt > 0:
            adjust_user_health_score(username, 0.2) # Micro reward for logging water
        elif amt < 0:
            adjust_user_health_score(username, -0.2) # Penalty for removing water
            
        water_target = int(user['weight_kg'] * 35) + (500 if user.get('daily_activity') in ['Moderate', 'Heavy'] else 0)
        updated_log = logs_collection.find_one({"username": username, "date": today})
        rewards = updated_log.get('rewards_tracked', {"water": False, "workout": False, "sleep": False, "calorie_penalty": False})
        
        if updated_log.get('water_drank_ml', 0) >= water_target and not rewards.get('water', False):
            adjust_user_health_score(username, 2.0) 
            logs_collection.update_one({"username": username, "date": today}, {"$set": {"rewards_tracked.water": True}})
    
    elif action_type == 'food':
        calories = int(value.get('calories', 0))
        food_name = value['name']
        if calories == 0: 
            calories = estimate_custom_calories(food_name)
            users_collection.update_one({"username": username}, {"$push": {"custom_learned_foods": {"name": food_name, "cals": calories, "tags": [], "time": ["Morning", "Afternoon", "Evening", "Night"]}}})
        logs_collection.update_one({"username": username, "date": today}, {"$inc": {"calories_eaten": calories}, "$push": {"foods_logged": f"{food_name} ({calories} kcal)"}})
        r_id = "meal_b" if hour < 11 else "meal_l" if hour < 16 else "snack" if hour < 19 else "meal_d"
        logs_collection.update_one({"username": username, "date": today, "routine.id": r_id}, {"$set": {"routine.$.done": True}})

        if calories >= 400:
            adjust_user_health_score(username, -0.5) # Penalty for heavy meal
        elif calories <= 200:
            adjust_user_health_score(username, 0.2)  # Reward for light/healthy meal

        calorie_target = int(10 * user['weight_kg'] + 6.25 * user['height_cm'] - 5 * user['age'])
        updated_log = logs_collection.find_one({"username": username, "date": today})
        rewards = updated_log.get('rewards_tracked', {"water": False, "workout": False, "sleep": False, "calorie_penalty": False})
        
        if updated_log.get('calories_eaten', 0) > (calorie_target + 300) and not rewards.get('calorie_penalty', False):
            adjust_user_health_score(username, -2.0) 
            logs_collection.update_one({"username": username, "date": today}, {"$set": {"rewards_tracked.calorie_penalty": True}})
        
    elif action_type == 'delete_food':
        log = logs_collection.find_one({"username": username, "date": today})
        if log and value in log.get('foods_logged', []):
            foods_list = log['foods_logged']
            foods_list.remove(value) 
            match = re.search(r'\((\d+)\s*kcal\)', value)
            if match:
                cal_val = int(match.group(1))
                logs_collection.update_one({"username": username, "date": today}, {"$set": {"foods_logged": foods_list}, "$inc": {"calories_eaten": -cal_val}})
                
                # Undo points if food deleted
                if cal_val >= 400:
                    adjust_user_health_score(username, 0.5)
                elif cal_val <= 200:
                    adjust_user_health_score(username, -0.2)
    
    elif action_type == 'workout':
        w_name = value.get('name')
        w_input = value.get('input')
        w_target = value.get('target')
        w_pct = float(value.get('pct', 100))
        
        log_string = f"{w_name}|{w_input}|{w_target}|{w_pct}"
        log = logs_collection.find_one({"username": username, "date": today})
        
        existing_log_str = None
        old_pct = 0
        for w in log.get('workouts_logged', []):
            if w.startswith(w_name + "|") or w.startswith(w_name + " - "):
                existing_log_str = w
                if "|" in w:
                    try: old_pct = int(w.split('|')[3])
                    except: old_pct = 100
                else: old_pct = 100
                break
                
        new_cal_burn = int(40 * (w_pct / 100.0))
        old_cal_burn = int(40 * (old_pct / 100.0))
        cal_diff = new_cal_burn - old_cal_burn
        
        if existing_log_str:
            logs_collection.update_one({"username": username, "date": today}, {"$pull": {"workouts_logged": existing_log_str}})
            
        logs_collection.update_one({"username": username, "date": today}, {"$push": {"workouts_logged": log_string}, "$inc": {"calories_eaten": -cal_diff}})
        
        if w_pct >= 80:
            adjust_user_health_score(username, 0.5) # Micro reward for logging a workout

        updated_log = logs_collection.find_one({"username": username, "date": today})
        total_exercises = len(updated_log.get('daily_locked_workout', {}).get('plan', []))
        fully_completed = 0
        for w in updated_log.get('workouts_logged', []):
            if "|" in w:
                try:
                    if int(w.split('|')[3]) >= 100: fully_completed += 1
                except: pass
            else: fully_completed += 1 
                
        is_circuit_done = (fully_completed >= total_exercises) and (total_exercises > 0)
        logs_collection.update_one({"username": username, "date": today, "routine.id": "workout_time"}, {"$set": {"routine.$.done": is_circuit_done}})

        rewards = updated_log.get('rewards_tracked', {"water": False, "workout": False, "sleep": False, "calorie_penalty": False})
        if is_circuit_done and not rewards.get('workout', False):
            adjust_user_health_score(username, 2.0) 
            logs_collection.update_one({"username": username, "date": today}, {"$set": {"rewards_tracked.workout": True}})

    elif action_type == 'sleep':
        sleep_hrs = float(value)
        logs_collection.update_one({"username": username, "date": today}, {"$set": {"sleep_hours": sleep_hrs}})
        logs_collection.update_one({"username": username, "date": today, "routine.id": "sleep_setup"}, {"$set": {"routine.$.done": True}})
        
        if sleep_hrs >= 7.0:
            adjust_user_health_score(username, 1.0) 
        elif 0 < sleep_hrs < 6.0:
            adjust_user_health_score(username, -1.0) # Penalty for poor sleep
        
    elif action_type == 'steps':
        step_amt = int(value)
        burned_calories = int(step_amt * 0.04) # 1 step = 0.04 kcal burn
        
        # 1. സ്റ്റെപ്പുകൾ കൂട്ടാനും കലോറി കുറയ്ക്കാനും ഉള്ള കോഡ് (Database Update)
        logs_collection.update_one(
            {"username": username, "date": today}, 
            {"$inc": {"steps": step_amt, "calories_eaten": -burned_calories}}
        )
        
        # 2. കലോറി മൈനസ് (0 ൽ താഴെ) ആവാതിരിക്കാൻ 
        updated_log = logs_collection.find_one({"username": username, "date": today})
        if updated_log and updated_log.get("calories_eaten", 0) < 0:
            logs_collection.update_one({"username": username, "date": today}, {"$set": {"calories_eaten": 0}})
        
        # 3. ഹെൽത്ത് സ്കോർ അപ്ഡേറ്റ് ചെയ്യാൻ
        if step_amt > 0:
            adjust_user_health_score(username, step_amt * 0.0005) # 1000 steps gives +0.5 score
        elif step_amt < 0:
            adjust_user_health_score(username, step_amt * 0.0005) # Reduces if steps are reset
    elif action_type == 'routine':
        is_done = value.get('done')
        logs_collection.update_one({"username": username, "date": today, "routine.id": value.get('id')}, {"$set": {"routine.$.done": is_done}})
        
        if is_done:
            adjust_user_health_score(username, 0.2)
        else:
            adjust_user_health_score(username, -0.2)
        
    return jsonify({"status": "success"}), 200

# ==========================================
# 8. ADVANCED ANALYTICS ENGINE
# ==========================================
@app.route('/api/analytics_data', methods=['POST'])
def get_analytics():
    username = request.get_json().get('username')
    user = users_collection.find_one({"username": username})
    if not user: return jsonify({"status": "error"}), 404
    
    logs = list(logs_collection.find({"username": username}).sort("date", 1))
    if not logs: return jsonify({"status": "error", "message": "No data available yet. Please interact with your dashboard to generate analytics."}), 404

    dates, water_data, calorie_data, sleep_data, steps_data = [], [], [], [], []
    for log in logs:
        dates.append(log['date'][5:]) 
        water_data.append(log.get('water_drank_ml', 0))
        calorie_data.append(log.get('calories_eaten', 0))
        sleep_data.append(log.get('sleep_hours', 0))
        steps_data.append(log.get('steps', 0))

    user_wt = user.get('weight_kg', 70)
    target_water = int(user_wt * 35)
    target_cals = int(10 * user_wt + 6.25 * user.get('height_cm', 170) - 5 * user.get('age', 25))

    today_log = logs[-1]
    
    # --- DYNAMIC DAILY INSIGHT GENERATION ---
    today_cals = today_log.get('calories_eaten', 0)
    today_water = today_log.get('water_drank_ml', 0)
    today_sleep = today_log.get('sleep_hours', 0)
    today_steps = today_log.get('steps', 0)
    
    # Calculate target steps dynamically for today
    activity_steps = {"Sitting": 5000, "Light": 7500, "Moderate": 10000, "Heavy": 12000}
    act_str = str(user.get('daily_activity', '')).lower()
    target_steps = 5000
    if "light" in act_str: target_steps = 7500
    elif "moderate" in act_str: target_steps = 10000
    elif "heavy" in act_str: target_steps = 12000

    today_workouts_count = len(today_log.get('workouts_logged', []))

    insight = "Based on your activity and dietary logging for <strong>today</strong>, here is your AI evaluation:<br><br>"

    # 1. Activity & Workout Check
    if today_steps > (target_steps * 2):
        insight += "⚠️ <strong>Overexertion Alert:</strong> Your physical activity is extremely high today. Ensure you consume enough electrolytes and rest well to prevent muscle breakdown.<br><br>"
    elif today_steps < (target_steps * 0.3) and today_workouts_count == 0:
        insight += "⚠️ <strong>Sedentary Alert:</strong> Very low physical activity today. Your metabolism needs movement to function optimally. Try to complete a short walk or a workout.<br><br>"
    elif today_workouts_count > 0 or today_steps >= target_steps:
        insight += "🔥 <strong>Active Metabolism:</strong> Excellent physical activity today! You are actively burning calories and keeping your metabolic rate high.<br><br>"
    else:
        insight += "🚶 <strong>Moderate Activity:</strong> You have some movement today, but hitting your step targets or completing a quick circuit will boost your results.<br><br>"

    # 2. Diet & Calorie Check
    if today_cals == 0:
        insight += "⚠️ <strong>No Food Logged:</strong> You haven't logged any meals today. Logging your food is crucial for AI tracking.<br><br>"
    elif today_cals > target_cals + 300:
        insight += "⚠️ <strong>Caloric Surplus:</strong> You have exceeded your daily calorie limit. Try to eat lighter for your next meal or do some extra cardio.<br><br>"
    elif today_cals < target_cals * 0.4:
        insight += "⚠️ <strong>Under-Eating Alert:</strong> Your caloric intake is currently very low. Make sure you are eating enough to sustain your energy.<br><br>"
    else:
        insight += "✅ <strong>Balanced Diet:</strong> Your caloric intake is perfectly aligned with your physical parameters today.<br><br>"

    # 3. Hydration Check
    if today_water > target_water + 1500:
        insight += "⚠️ <strong>Over-Hydration Warning:</strong> You are consuming an excessive amount of water. This can dilute essential electrolytes like sodium in your body.<br><br>"
    elif today_water < target_water * 0.4:
        insight += "⚠️ <strong>Dehydration Risk:</strong> Your water intake is critically low. Please drink more water to process your meals properly.<br><br>"
    elif today_water >= target_water:
        insight += "💧 <strong>Optimal Hydration:</strong> Great job hitting your daily water targets!<br><br>"
    else:
        insight += "🚰 <strong>Hydration Needed:</strong> You are on track, but still need a bit more water to hit your optimal daily target.<br><br>"

    # 4. Sleep/Recovery Check
    if today_sleep > 10:
        insight += "⚠️ <strong>Oversleeping Alert:</strong> You slept for more than 10 hours. Excessive sleep can sometimes cause lethargy and slow down daytime metabolism.<br><br>"
    elif today_sleep == 0:
        insight += "⏳ <strong>Pending Recovery:</strong> Don't forget to log your sleep tomorrow morning for a complete recovery analysis.<br><br>"
    elif today_sleep < 6.5:
        insight += f"⚠️ <strong>Recovery Deficit:</strong> Your sleep duration ({today_sleep} hrs) is sub-optimal for muscle recovery.<br><br>"
    else:
        insight += f"✅ <strong>Optimal Recovery:</strong> Your sleep cycle ({today_sleep} hrs) is perfectly maintained.<br><br>"
    # ----------------------------------------

    today_stats = {
        "calories": {"current": today_cals, "target": target_cals},
        "water": {"current": today_water, "target": target_water},
        "sleep": {"current": today_sleep, "target": 8},
        "steps": {"current": today_steps, "target": target_steps} 
    }

    today_foods = list(today_log.get('foods_logged', []))
    today_foods.reverse()
    
    today_workouts = []
    for w in today_log.get('workouts_logged', []):
        w_name = w.split('|')[0].strip() if '|' in w else w.split('-')[0].strip()
        if w_name not in today_workouts: today_workouts.append(w_name)
    today_workouts.reverse()

    total_days = len(logs)
    days_with_workouts = sum(1 for l in logs if len(l.get('workouts_logged', [])) > 0)
    workout_consistency = round((days_with_workouts / total_days * 100) if total_days > 0 else 0)

    overall_stats = {
        "avg_cals": round(sum(calorie_data) / total_days) if total_days else 0,
        "avg_water": round(sum(water_data) / total_days) if total_days else 0,
        "avg_sleep": round(sum(sleep_data) / total_days, 1) if total_days else 0,
        "consistency": workout_consistency
    }

    history_insight = f"Over the recorded period of <strong>{total_days} days</strong>, you have maintained a workout compliance rate of <strong>{workout_consistency}%</strong>."

    return jsonify({
        "status": "success", "today": today_stats, "overall": overall_stats, "dates": dates, 
        "charts": {"water": water_data, "calories": calorie_data, "sleep": sleep_data, "steps": steps_data},
        "insight": insight, "history_insight": history_insight, "today_foods": today_foods, "today_workouts": today_workouts
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)