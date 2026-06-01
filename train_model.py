import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

print("⚙️ Loading the dataset...")
# 1. Load the generated dataset
df = pd.read_csv('metabolic_dataset.csv')

# 2. Convert text data into numbers (Machine Learning models only understand numbers!)
activity_map = {"Sitting": 1, "Light": 2, "Moderate": 3, "Heavy": 4}
df['Activity_Level'] = df['Activity_Level'].map(activity_map)

# 3. Define the Features (Inputs) and Target (Output)
X = df[['Age', 'Height_cm', 'Weight_kg', 'BMI', 'Activity_Level', 'Sleep_Hours', 'Water_Intake_ml', 'Healthy_Food_Count', 'Junk_Food_Count']]
y = df['Target_Health_Score']

# 4. Train the Random Forest AI Model
print("🧠 Training the AI Brain... (This might take a few seconds)")
ai_model = RandomForestRegressor(n_estimators=100, random_state=42)
ai_model.fit(X, y)

# 5. Save the trained model as a file
joblib.dump(ai_model, 'ai_brain.pkl')
print("✅ AI Brain successfully trained and saved as 'ai_brain.pkl'!")