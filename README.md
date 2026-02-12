# 🛒 End-to-End E-commerce ETL & Customer Segmentation Pipeline

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

---

## 📌 Project Overview

This project is a full-stack **Data Engineering and Business Intelligence solution** that automates the extraction of e-commerce data, processes it using Machine Learning for customer segmentation (K-Means Clustering), stores it in a relational database, and visualizes insights via an interactive dashboard.

### 🎯 Key Business Questions Answered

- **Who are our most valuable customers?** (Identified via clustering)
- **Which product categories drive the most revenue vs. volume?**
- **How do discount strategies impact different customer segments?**
- **What are the seasonal purchasing trends across various categories?**

---

## 🏗️ System Architecture

The pipeline is designed with a modular architecture to ensure scalability and maintainability.

### 🔄 Pipeline Flow

1. **Extraction**
   - Automated data retrieval from Kaggle using `kagglehub`.

2. **Transformation**
   - Data cleaning and type conversion
   - Feature engineering using `pandas`
   - Customer segmentation using K-Means clustering (`k = 7`)

3. **Machine Learning**
   - Customer segmentation using `scikit-learn` K-Means.

4. **Loading**
   - Processed data pushed to a **PostgreSQL 17** database using `SQLAlchemy`.

5. **Visualization**
   - Interactive **Streamlit** dashboard for business stakeholders.

---

## 📂 Project Structure

```text
ecommerce-etl-pipeline/
├── src/                # Modular ETL logic
│   ├── __init__.py     # Package initialization
│   ├── extract.py      # Kaggle data ingestion
│   ├── transform.py    # Cleaning & K-Means Clustering
│   └── load.py         # PostgreSQL database loading
├── dashboard/          # BI Layer
│   └── app.py          # Streamlit dashboard code
├── data/               # Local data storage (Gitignored)
├── main.py             # Orchestration script (Entry point)
├── .env                # Database credentials (Protected)
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

Ensure the following are installed:

- **Python 3.9+**
- **PostgreSQL 17**
  - A local instance running
  - A database created (e.g., `ecommerce_db`)
- **Kaggle Account**
  - Download your `kaggle.json` API token
  - Place it in:
    ```
    ~/.kaggle/kaggle.json
    ```

---

### 2️⃣ Installation & Environment Setup

Clone the repository and set up your virtual environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/ecommerce-etl-pipeline.git
cd ecommerce-etl-pipeline

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# Install required libraries
pip install -r requirements.txt
```

---

### 3️⃣ Database & Secret Configuration

Create a `.env` file in the root directory of the project to securely store database credentials.

> ⚠️ This file should NOT be committed to Git.

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASS=your_password_here
```

---

### 4️⃣ Running the ETL Pipeline

Before launching the dashboard, run the full pipeline to extract, transform, and load data into PostgreSQL:

```bash
python3 main.py
```

This script will:

- Download the dataset from Kaggle
- Clean and transform the data
- Perform K-Means clustering (`k = 7`)
- Create the `ecommerce_sales` table in PostgreSQL

---

### 5️⃣ Launching the BI Dashboard

Once the pipeline runs successfully, start the Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

The dashboard will open automatically in your browser at:

```
http://localhost:8501
```

---