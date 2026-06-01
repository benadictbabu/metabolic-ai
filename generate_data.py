import pandas as pd
import numpy as np
import random

# Number of synthetic records to generate
NUM_RECORDS = 5000

print(f"⚙️ Generating {NUM_RECORDS} artificial user records...")

data = []

for _ in range(NUM_RECORDS):
    # 1. Basic Demographics
    age = random.randint(18, 65)
    height_cm = random.randint(140, 200)
    
    # Generate realistic weight based on height (with some randomness for overweight/underweight)
    ideal_weight = (height_cm - 100)
    weight_kg = round(random.uniform(ideal_weight - 20, ideal_weight + 40), 1)
    
    # Calculate actual BMI
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 1)
    
    # 2. Lifestyle Habits
    activity_level = random.choice(["Sitting", "Light", "Moderate", "Heavy"])
    sleep_hours = random.choice([4, 5, 6, 7, 8, 9])
    water_intake_ml = random.randint(1000, 4500)
    
    # Dietary habit simulation
    healthy_foods = random.randint(0, 5) # Number of healthy foods they usually eat
    junk_foods = random.randint(0, 3)    # Number of junk foods they usually eat
    
    # 3. Mathematical Formula to determine the "True Health Score" (Target for ML)
    # Start with a baseline of 100 and subtract points for bad habits
    health_score = 100
    
    # BMI Penalty
    if bmi < 18.5 or bmi > 25.0:
        health_score -= (abs(22.0 - bmi) * 1.5) # Penalty grows the further they are from ideal BMI 22
        
    # Activity Penalty/Bonus
    if activity_level == "Sitting": health_score -= 15
    elif activity_level == "Light": health_score -= 5
    elif activity_level == "Heavy": health_score += 5
    
    # Sleep Penalty
    if sleep_hours < 7: health_score -= ((7 - sleep_hours) * 5)
    
    # Hydration Penalty
    if water_intake_ml < 2500: health_score -= 10
    
    # Nutrition Impact
    health_score += (healthy_foods * 2)
    health_score -= (junk_foods * 5)
    
    # Clamp the final score between 10 and 100
    health_score = max(10, min(100, round(health_score)))
    
    # Categorize the target class for the AI to predict
    if health_score >= 80:
        health_status = "Optimal"
    elif health_score >= 60:
        health_status = "Good"
    elif health_score >= 40:
        health_status = "Moderate Risk"
    else:
        health_status = "High Risk"

    # Append to dataset
    data.append({
        "Age": age,
        "Height_cm": height_cm,
        "Weight_kg": weight_kg,
        "BMI": bmi,
        "Activity_Level": activity_level,
        "Sleep_Hours": sleep_hours,
        "Water_Intake_ml": water_intake_ml,
        "Healthy_Food_Count": healthy_foods,
        "Junk_Food_Count": junk_foods,
        "Target_Health_Score": health_score,
        "Target_Status": health_status
    })

# Convert to a Pandas DataFrame and save as CSV
df = pd.DataFrame(data)
df.to_csv("metabolic_dataset.csv", index=False)

print("✅ Dataset successfully created: 'metabolic_dataset.csv'")
print(df.head()) # Preview the first 5 rows