# 📈 Dynamic Pricing & Revenue Optimization Engine
<img width="1911" height="1055" alt="dashboard png" src="https://github.com/user-attachments/assets/ad69a3de-c9e1-4797-af40-edde269c63ab" />

## 🚀 Overview
The **Dynamic Pricing & Revenue Optimization Engine** is a full-stack Python web application designed to simulate and optimize corporate pricing strategies. Moving beyond historical data reporting, this engine mathematically models the **Price Elasticity of Demand (PED)** and provides an interactive executive dashboard to forecast the financial impact of active pricing decisions.

This project bridges the gap between raw statistical modeling and actionable business intelligence, proving the ability to handle an end-to-end data lifecycle: from synthetic data architecture and backend regression modeling to frontend UI deployment.

## 🛠️ Tech Stack
* **Frontend & Deployment:** Streamlit
* **Data Engineering & Wrangling:** Python, Pandas, NumPy
* **Statistical Modeling:** Statsmodels (Log-Log Regression)

## 🧠 Core Architecture & Features

### 1. Hyper-Realistic Data Generation Pipeline
Standard synthetic data relies on uniform distributions, which fail to mimic real market behavior. This engine utilizes a custom Python pipeline to generate 1 year of daily transactional data (over 18,000 rows) that behaves authentically by injecting:
* **Mathematical Elasticity:** Sales volume is strictly bound to price fluctuations using underlying demand curves.
* **Sinusoidal Seasonality:** Baseline volume rises and falls based on a continuous sine wave, peaking during Q4 to simulate holiday demand.
* **Gaussian Noise:** Real-world variance is simulated using normal distribution multipliers (`np.random.normal`) to prevent artificial uniformity.

### 2. Statistical Modeling (Price Elasticity)
The application dynamically calculates the price sensitivity of 5 distinct product categories.
* It utilizes **Ordinary Least Squares (OLS) Log-Log regression** to approximate constant elasticity percentages.
* Products are mathematically categorized as elastic or inelastic, directly driving the projected volume in the simulation engine.

### 3. Interactive Executive Dashboard
Built natively in Streamlit, the frontend translates complex statistical outputs into a scannable, business-facing UI.
* **"What-If" Simulation:** Stakeholders can adjust a global pricing parameter (-20% to +20%) to immediately view projected changes in sales volume and total gross margin.
* **Real-Time Variance Tracking:** The UI instantly recalculates and displays the exact dollar amount of profit variance against the baseline historical data.

## 💻 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/dynamic-pricing-engine.git](https://github.com/yourusername/dynamic-pricing-engine.git)
   cd dynamic-pricing-engine
