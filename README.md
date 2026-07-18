# ⚽ xG Analytics Dashboard & Match Day Simulator

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://xg-analytics-dashboard.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge\&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge\&logo=streamlit)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-green?style=for-the-badge)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-blueviolet?style=for-the-badge)
![License](https://img.shields.io/github/license/harshskarki/xg-analytics-dashboard?style=for-the-badge)

---

# ⚽ xG Analytics Dashboard & Match Day Simulator

An advanced football analytics platform that combines **Machine Learning**, **Interactive Data Visualization**, and **Game Development** into a single immersive experience.

Built using **Python, Streamlit, Plotly, and XGBoost**, the application allows users to explore how different match situations influence scoring probability through real-time Expected Goals (xG) predictions and interactive simulations.

🌐 **Live Demo:**
https://xg-analytics-dashboard.streamlit.app/

---

## 📸 Project Preview

> Add screenshots or GIFs here showcasing:
>
> * Interactive Pitch
> * xG Prediction Panel
> * PSxG Goal Visualizer
> * Heatmaps
> * Penalty Mini-Game

---

## ✨ Key Features

### ⚽ AI-Powered xG Prediction Engine

Predict the probability of a shot becoming a goal using an XGBoost machine learning model trained on realistic football scenarios.

### 📊 Interactive Analytics Dashboard

Analyze shooting outcomes through dynamic charts, graphs, and visualizations powered by Plotly.

### 🎯 Interactive Shot Simulator

Experiment with different:

* Shot locations
* Body parts
* Assist types
* Defensive pressure levels

and instantly see how goal probability changes.

### 🔥 Goal Probability Heatmaps

Visualize dangerous attacking zones and identify the areas with the highest scoring likelihood.

### 🥅 Post-Shot xG (PSxG) Goal Simulator

Evaluate goalkeeper difficulty and save probability based on:

* Shot height
* Shot width
* Shot placement

### 🎙️ AI Match Commentary

Generate dynamic commentary describing your shot scenario in real time.

Examples:

* "A thunderous strike from distance!"
* "The keeper had absolutely no chance."
* "Perhaps a pass would've been the smarter choice."

### 🎮 Penalty Flick Mini-Game

Challenge an AI goalkeeper in a fast-paced HTML5 penalty shootout game directly inside the dashboard.

### 📈 Real-Time Data Visualizations

* Scatter Plots
* Density Heatmaps
* Shot Maps
* Goal Probability Curves
* Interactive Pitch Graphics

### 📱 Fully Responsive Interface

Optimized for desktop, tablet, and mobile devices.

---

## 🛠️ Tech Stack

### Frontend

* Streamlit
* Plotly
* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Pandas
* NumPy

### Machine Learning

* XGBoost
* Scikit-Learn

### Visualization

* Matplotlib
* Plotly

---

## 🧠 Machine Learning Pipeline

The xG engine is powered by an XGBoost classifier trained on a synthetic football dataset containing thousands of simulated shots.

### Feature Engineering

The model calculates:

* Distance to Goal
* Shot Angle
* Defender Pressure
* Assist Type
* Body Part Used
* Shot Coordinates

### Mathematical Modeling

The dashboard computes:

* Goal Visibility Angle
* Euclidean Distance
* Goalkeeper Reach Zones
* Shooting Difficulty Scores

These features are then fed into an XGBoost model to predict the likelihood of a goal.

### Output

The model returns an Expected Goals (xG) score between:

```text
0.00 → Extremely unlikely to score
1.00 → Almost certain goal
```

---

## 🚀 How to Run Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/harshskarki/xg-analytics-dashboard.git
cd xg-analytics-dashboard
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Launch the Application

```bash
python -m streamlit run app.py
```

### 4️⃣ Open in Browser

```text
http://localhost:8501
```

---

## 📂 Project Structure

```text
xg-analytics-dashboard/
│
├── app.py
├── requirements.txt
├── model/
├── assets/
├── data/
├── utils/
├── visualizations/
├── README.md
│
└── mini_game/
```

---

## 🎯 Learning Outcomes

Through this project I explored:

* Machine Learning Model Development
* Sports Analytics
* Feature Engineering
* Interactive Data Visualization
* Streamlit Application Development
* XGBoost Classification Models
* HTML5 Game Development
* User Experience Design
* Data Storytelling

---

## 🔮 Future Improvements

* Real Match Dataset Integration
* Player-Specific xG Models
* Team Performance Analytics
* Match Outcome Predictions
* Shot Clustering Analysis
* Tactical Passing Networks
* Expected Assists (xA)
* Multi-League Comparisons
* Live Match Data Integration
* AI Match Simulation Engine

---

## 👨‍💻 Author

**Harshvardhan Singh Karki**

B.Tech CSE '27 | Software Engineering & Full-Stack Developer

GitHub: https://github.com/harshskarki

---

## ⭐ Support

If you found this project useful, consider giving it a star on GitHub.

It helps support future development and encourages more open-source football analytics projects.
