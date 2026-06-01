
---

# 🧬 Metabolic AI: Advanced Health Tracking & Analytics

**An Intelligent Real-Time Metabolic Evaluation Dashboard**

Metabolic AI is a dynamic, data-driven web application built with Python (Flask) and MongoDB. It acts as an autonomous digital health coach that tracks daily habits (hydration, sleep, steps, and caloric intake) and uses advanced algorithmic logic to calculate a real-time "Health Score." Based on this score and recent behavior, the AI dynamically generates adaptive workout circuits and highly personalized executive health summaries.

---

## 🚀 Key Features

* **Intelligent Onboarding:** Calculates baseline BMI and metabolic efficiency based on age, weight, height, activity level, and dietary preferences.
* **Real-Time Health Score:** A highly sensitive algorithm that adjusts the user's score via "micro-rewards" and penalties instantly upon logging actions.
* **Adaptive AI Workouts:** Generates custom workout circuits dynamically (e.g., triggering "Fatigue Recovery Mode" if sleep is low, or "Calorie Burn Loaded" if overfed).
* **Smart Combo Analytics:** Detects contradictory habits (e.g., sedentary lifestyle + heavy carbohydrate intake) and applies logical health adjustments.
* **Premium Dashboard UI:** A stunning dark-mode "glassmorphism" interface built with Tailwind CSS, featuring gradient animations, ambient backgrounds, and contextual AI suggestions.

---

## 🛠️ Technology Stack

* **Frontend:** HTML5, Tailwind CSS (via CDN), Vanilla JavaScript.
* **Backend:** Python 3.x, Flask (REST API Routing, Session handling).
* **Database:** MongoDB (NoSQL) for fast, flexible logging of daily metrics.
* **Security:** `werkzeug.security` for password hashing.
* **Machine Learning Environment:** Joblib, Scikit-learn (Support for external AI models).

---

## ⚙️ Setup & Installation Guide

Follow these steps carefully to set up the project on your local machine.

### 1. Prerequisites

Ensure you have the following installed on your system:

* **Python (3.8 or higher):** [Download Python](https://www.python.org/downloads/)
* **MongoDB:** [Download MongoDB Community Server](https://www.mongodb.com/try/download/community). (Make sure the MongoDB service is running on your machine).

### 2. Clone the Repository

Download or clone this project folder to your local machine.

```bash
git clone <your-repository-url>
cd metabolic-ai

```

### 3. Create a Virtual Environment (Highly Recommended)

It is best practice to run Python projects in an isolated environment so dependencies do not conflict.

* **Windows:**
```bash
python -m venv venv
venv\Scripts\activate

```


* **Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate

```



### 4. Install Required Python Packages

Once the virtual environment is activated, install the necessary libraries using `pip`.

```bash
pip install Flask pymongo werkzeug joblib scikit-learn

```

*(Note: If you have a `requirements.txt` file, you can run `pip install -r requirements.txt`)*

### 5. Verify MongoDB Connection

Ensure MongoDB is running locally on the default port `27017`. The application connects to it automatically via the URI: `mongodb://localhost:27017/`.

* The database `metabolic_ai_core` and collections (`users`, `daily_metrics`) will be created automatically upon your first registration.

---

## 💻 Running the Application

1. **Start the Flask Server:**
In your terminal (with the virtual environment activated), run the main application file:
```bash
python app.py

```


2. **Access the Web App:**
Once the server starts, you will see output indicating the server is running (e.g., `* Running on http://127.0.0.1:5000`).
* Open your web browser (Chrome/Edge/Safari).
* Go to: **`http://127.0.0.1:5000`**



---

## 📖 How to Use the Application (User Flow)

1. **Registration (`/`):** Create a new account on the landing page using a secure username and password.
2. **AI Clinical Onboarding (`/onboarding`):**
Input your physical metrics (Age, Weight, Height), daily activity level, and select the types of food you usually eat.
3. **Master Plan (`/masterplan`):**
The AI will calculate your initial baseline Health Score (from 10 to 100) and provide a tailored risk evaluation (e.g., "Elite Metabolism", "Moderate Risk").
4. **The Dashboard (`/dashboard`):**
* Use the widgets to log water intake, custom foods, sleep hours, and steps.
* Watch your **Health Score** update in real-time as you log positive actions or incur penalties for overeating.
* Click **Update/Done** on the dynamically generated AI Workout Circuit.


5. **Analytics (`/analytics`):**
Click the "Analytics" button on the dashboard navbar to view an Executive Summary. If you have been sedentary, under-eating, or dehydrated, the AI Coach will warn you here based strictly on your day's inputs.

---

## 🧩 Project Structure

```text
metabolic-ai/
│
├── app.py                # Main backend server (Flask logic, MongoDB routes)
├── ai_brain.pkl          # (Optional) Pre-trained ML model file
├── recommender.py        # Food recommendation logic script
│
├── templates/            # Frontend HTML Files
│   ├── index.html        # Login/Registration
│   ├── onboarding.html   # User setup & data collection
│   ├── masterplan.html   # Initial AI Baseline Score reveal
│   ├── dashboard.html    # Main dynamic tracking interface
│   └── analytics.html    # Daily AI executive summary
│
└── README.md             # Project documentation

```

---

## ⚠️ Troubleshooting

* **"Database connection failed" error in terminal:** Ensure MongoDB is installed, the service is running, and it is accessible at `localhost:27017`.
* **Changes in `app.py` aren't reflecting:** Press `Ctrl + C` in the terminal to stop the server, then run `python app.py` again.
* **Health Score stuck at the same number?** Ensure you are logging entirely new actions. The app implements "Smart Combos"—logging heavy carbs when your activity is "Sitting" will penalize you, while walking will boost your score incrementally.

---

