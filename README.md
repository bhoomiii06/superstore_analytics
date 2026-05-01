# 📊 Superstore Profit Analytics: End-to-End Business Insights

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://superstoreanalytics-sales.streamlit.app/)

**Live Application:** [Explore the Interactive Dashboard Here](https://superstoreanalytics-sales.streamlit.app/)

---

## 🎯 Executive Abstract
Developed as part of a TCS iON Industry Project, this analytics web application tackles real-world profitability challenges for a national retail superstore. By processing and analyzing four years of historical transactional data, this project identifies critical areas of financial bleed and provides interactive, data-driven insights to help executive management optimize discounting and sales strategies.

## 🔍 Multi-Dimensional Analysis
To provide a comprehensive view of business health, the data was investigated across four key domains:
* **Financial Analysis:** Evaluated the direct impact of discount structures on profit margins and identified baseline profitability thresholds.
* **Geospatial Analysis:** Mapped sales and profit distribution across the US to isolate high-performing regions and pinpoint state-level financial bleed.
* **Customer Segmentation:** Analyzed purchasing behaviors, shipping preferences, and profitability across Consumer, Corporate, and Home Office tiers.
* **Product Performance:** Ranked categories and sub-categories to reveal how high-margin technology products cross-subsidize losses in furniture and office supplies.

## 📈 Key Business Results & Insights
* **The "Discount Dilemma":** The data reveals a direct negative correlation between aggressive discounting and profitability. Discounts exceeding 20% consistently result in negative profit margins, driving entire categories (specifically *Furniture*) into net losses.
* **Geographical Bleed:** High-volume states such as Texas, Pennsylvania, and Illinois exhibit a dangerous trend: they rank in the Top 10 for total sales volume but operate at a severe net loss due to localized over-discounting.
* **Product Subsidization:** The *Technology* category (e.g., Copiers, Phones) acts as the primary profit engine. Despite having lower overall order quantities than Office Supplies, these high-margin items are cross-subsidizing the heavy losses incurred in other sectors.
* **Operational Efficiency:** Same-day shipping accounts for only 5.25% of total orders. The business can reduce operational overhead by optimizing warehouse staffing around Standard and Second-Class fulfillment schedules, which make up the vast majority of deliveries.

## 🛠️ The Analytical Process
1. **Data Extraction & Quality Assurance (Python/Pandas):** 
   * Validated data integrity by handling missing values, removing duplicates, and standardizing formats.
   * Engineered new business KPIs including `Profit Margin (%)` and `Shipping Duration`.
2. **Database Aggregation (MS SQL Server):** 
   * Designed advanced T-SQL queries utilizing Common Table Expressions (CTEs) and Window Functions to extract segmented customer and geographical metrics.
3. **Interactive Visualization (Plotly):** 
   * Built interactive sunburst charts, heatmaps, and scatter plots to replace static, traditional dashboards.
4. **Web Deployment (Streamlit):** 
   * Engineered and deployed a multi-page Python web application to surface insights directly to stakeholders via the cloud.

## 💻 Tech Stack
* **Languages:** Python 3.x, T-SQL
* **Data Processing & QA:** Pandas, NumPy
* **Visualization:** Plotly Express, Plotly Graph Objects, Power BI
* **Web Framework:** Streamlit
* **Database:** MS SQL Server

## How to Run the Application
There are two primary ways to run and interact with this project: via the live cloud deployment or locally on your own machine.

**Method 1: Live Cloud Deployment (Recommended for Viewing)**
The application is deployed on Streamlit Community Cloud and is automatically updated whenever new code is pushed to the main branch of this repository.

Access the App: Simply navigate to https://superstoreanalytics-sales.streamlit.app/ in any modern web browser.

Interact: Use the sidebar navigation to switch between dashboards and adjust the global filters (Year, Region) to dynamically explore the data. No installation or setup is required.

**Method 2: Local Installation (For Development & Testing)**
If you would like to run this project on your local machine to explore the code or make modifications, follow these steps:

**Clone the repository:**

Bash
git clone [https://github.com/](https://github.com/)<your-github-username>/<your-repo-name>.git
cd <your-repo-name>
Create a virtual environment & activate it:
It is highly recommended to use a virtual environment to manage dependencies without affecting your system Python installation.

Bash

python -m venv venv

## On Windows:
venv\Scripts\activate

## On Mac/Linux:
source venv/bin/activate
Install dependencies:
Install the required Python packages listed in the requirements file.

Bash

pip install -r requirements.txt
Launch the application:
Start the Streamlit server locally.

Bash
   streamlit run app.py
---

## 📁 Project Structure
```text
├── data/
│   ├── Superstore Dataset.csv   # Raw dataset
│   └── Final_Analysis.csv       # Cleaned and engineered dataset used by the app
├── notebooks/
│   └── sales.ipynb              # Jupyter Notebook with EDA and data pipeline logic
├── sql/
│   └── sqlQuery.sql             # Advanced SQL queries for database-level aggregations
├── app.py                       # Main Streamlit application script
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
