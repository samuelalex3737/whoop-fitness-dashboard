# 🏋️ WHOOP Fitness Analytics Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

**Advanced Data Visualization Dashboard for Fitness Analytics**

*University Final Project - Data Visualization*

[🚀 Live Demo](#deployment) · [📊 Features](#features) · [🛠️ Installation](#installation) · [🐳 Docker](#docker-deployment)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Dataset](#dataset)
- [Installation](#installation)
- [Docker Deployment](#docker-deployment)
- [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Technologies Used](#technologies-used)

---

## 🎯 Overview

This comprehensive dashboard provides advanced analytics and visualizations for WHOOP fitness tracker data. Built with Streamlit and Plotly, it offers interactive exploration of 100,000+ fitness records with machine learning insights.

### Key Highlights

- 📊 **15+ Advanced Chart Types** - Treemaps, Sunbursts, Heatmaps, Radar, Waterfall, and more
- 🧠 **Machine Learning Integration** - K-Means clustering, RFM analysis, association mining
- 🔮 **What-If Analysis** - Interactive scenario simulation
- 🐳 **Docker Ready** - One-command deployment
- ☁️ **Streamlit Cloud Compatible** - Easy hosting on Streamlit

---

## ✨ Features

### 📈 Visualization Types

| Chart Type | Purpose | Insight |
|------------|---------|---------|
| **Treemap** | Hierarchical activity breakdown | Shows calorie distribution across fitness levels, sports, and activities |
| **Sunburst** | Multi-level categorical drilling | Reveals demographic patterns in workout preferences |
| **Dual-Axis Charts** | Correlate two metrics | Displays recovery vs strain inverse relationship |
| **Heatmaps** | Seasonal & temporal patterns | Identifies optimal training days and seasons |
| **Waterfall** | Cumulative contribution | Shows how each activity adds to total calorie burn |
| **Violin Plots** | Distribution comparison | Compares recovery variability across fitness levels |
| **Box Plots** | Statistical summary | Analyzes sleep stage distributions |
| **Radar Charts** | Multi-metric profiles | Compares activity types across performance dimensions |
| **Pareto Chart** | 80/20 analysis | Identifies top calorie-burning activities |
| **Growth-Share Matrix** | BCG-style quadrants | Classifies activities as Stars, Cows, Dogs, or Question Marks |
| **Doughnut Charts** | Proportional breakdown | Shows recovery zone and fitness level distributions |

### 🧠 Advanced Analytics

- **RFM Analysis with K-Means Clustering** - Segments users by workout behavior (Recency, Frequency, Monetary)
- **Confusion Matrix** - Sleep quality vs recovery category analysis
- **Cohort Retention Map** - Tracks user workout consistency over time
- **What-If Scenarios** - Simulates sleep and training load impacts
- **Association Rule Mining** - Discovers behavior patterns (Apriori-style)
- **Activity Co-occurrence Matrix** - Identifies common workout combinations

---

## 📊 Dataset

The dashboard uses WHOOP fitness data with the following structure:

| Column | Description |
|--------|-------------|
| `user_id` | Unique user identifier |
| `date` | Activity date |
| `recovery_score` | Daily recovery percentage (0-100) |
| `day_strain` | Total daily strain (0-21) |
| `sleep_hours` | Total sleep duration |
| `sleep_efficiency` | Sleep quality percentage |
| `hrv` | Heart Rate Variability (ms) |
| `resting_heart_rate` | Resting HR (bpm) |
| `activity_type` | Type of workout |
| `activity_strain` | Workout strain score |
| `activity_calories` | Calories burned during workout |
| `hr_zone_*_min` | Time in each heart rate zone |
| ...and 25+ more metrics |

**Dataset Size:** 100,000 records × 39 columns

---

## 🛠️ Installation

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- Git

### Local Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/whoop-fitness-dashboard.git
   cd whoop-fitness-dashboard
   ```

2. **Create Virtual Environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Dashboard**
   ```bash
   streamlit run app.py
   ```

5. **Open Browser**
   Navigate to `http://localhost:8501`

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and run with one command
docker-compose up --build

# Run in detached mode
docker-compose up -d --build

# Stop the container
docker-compose down
```

### Using Docker CLI

```bash
# Build the image
docker build -t whoop-dashboard .

# Run the container
docker run -p 8501:8501 whoop-dashboard

# Run in detached mode
docker run -d -p 8501:8501 --name whoop-dashboard whoop-dashboard
```

### Docker Desktop

1. Open Docker Desktop
2. Navigate to project folder
3. Run `docker-compose up --build`
4. Access dashboard at `http://localhost:8501`

---

## ☁️ Streamlit Cloud Deployment

### Step 1: Push to GitHub

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: WHOOP Fitness Dashboard"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/whoop-fitness-dashboard.git

# Push to GitHub
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `whoop-fitness-dashboard`
5. Set main file path: `app.py`
6. Click "Deploy!"

### Step 3: Share Your Dashboard

Your dashboard will be available at:
```
https://YOUR_USERNAME-whoop-fitness-dashboard-app-xxxxx.streamlit.app
```

---

## 📁 Project Structure

```
whoop-fitness-dashboard/
│
├── app.py                    # Main Streamlit application
├── whoop_fitness.csv         # Dataset (100K records)
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── README.md                # Documentation
│
└── .streamlit/
    └── config.toml          # Streamlit theme configuration
```

---

## 🖼️ Dashboard Sections

### 1. 🌳 Overview & Treemap
- Hierarchical treemap of activity distribution
- Multi-level sunburst chart
- Recovery and fitness level doughnut charts

### 2. 📈 Trends & Dual-Axis
- Recovery vs Strain time series
- HRV & Sleep correlation
- Waterfall calorie breakdown

### 3. 🔥 Heatmaps & Seasons
- Seasonal strain patterns
- Sleep quality temporal analysis
- Heart rate zone distribution

### 4. 🎯 Advanced Charts
- Violin plots for distributions
- Box plots for sleep stages
- Radar charts for activity profiles
- Pareto (80/20) analysis
- BCG Growth-Share matrix

### 5. 🧠 ML & Clustering
- RFM segmentation with K-Means
- 3D cluster visualization
- Confusion matrix analysis
- Cohort retention analysis

### 6. 🔮 What-If Analysis
- Sleep impact simulator
- Training load optimizer
- Scenario comparisons
- Goal-based recommendations

### 7. 📊 Association Mining
- Discovered behavior patterns
- Activity co-occurrence matrix
- Metric correlation network

---

## 🔧 Technologies Used

| Category | Technology |
|----------|------------|
| **Framework** | Streamlit 1.31 |
| **Visualization** | Plotly 5.18, Seaborn, Matplotlib |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn, SciPy |
| **Association Mining** | MLxtend (Apriori) |
| **Containerization** | Docker, Docker Compose |
| **Hosting** | Streamlit Cloud |

---

## 📝 License

This project is created for educational purposes as a University Final Project.

---

## 👤 Author

**Samuel**

- University Final Project - Data Visualization
- January 2026

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ using Streamlit

</div>
