import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# 1. Setup & Database Connection
load_dotenv()

def get_data():
    user = os.getenv("DB_USER")
    pw = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT") or "5432"
    db = os.getenv("DB_NAME")
    
    engine = create_engine(f'postgresql://{user}:{pw}@{host}:{port}/{db}')
    query = "SELECT * FROM ecommerce_sales"
    df = pd.read_sql(query, engine)
    
    # Ensure purchase_date is datetime for the line chart
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    return df

# 2. Page Configuration
st.set_page_config(page_title="E-commerce Cluster Insights", layout="wide")
st.title("📊 E-commerce Customer Segmentation Dashboard")

try:
    df = get_data()

    # --- Sidebar Filters ---
    st.sidebar.header("Global Filters")
    category_list = df['category'].unique()
    selected_categories = st.sidebar.multiselect("Select Categories:", options=category_list, default=category_list)
    
    df_selection = df[df['category'].isin(selected_categories)]

    # --- Create Tabs ---
    tab1, tab2 = st.tabs(["📈 General Business Insights", "🤖 Customer Segmentation (AI)"])

    # --- TAB 1: GENERAL INSIGHTS ---
    with tab1:
        st.header("General Business Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Which category is most bought over time?")
            # Count of purchases per category over time
            category_trend = df_selection.groupby([pd.Grouper(key='purchase_date', freq='M'), 'category']).size().reset_index(name='units_sold')
            fig_trend = px.line(category_trend, x="purchase_date", y="units_sold", color="category", markers=True)
            st.plotly_chart(fig_trend, use_container_width=True)
            
        with col2:
            st.subheader("Which category generates the most revenue?")
            # Sum of final_price per category
            category_revenue = df_selection.groupby('category')['final_price'].sum().sort_values(ascending=False).reset_index()
            fig_rev = px.bar(category_revenue, x='category', y='final_price', color='final_price', color_continuous_scale='Greens')
            st.plotly_chart(fig_rev, use_container_width=True)

        st.divider()
        
        # Payment Method Analysis (Additional Insight)
        st.subheader("Preferred Payment Methods")
        pay_method = df_selection['payment_method'].value_counts().reset_index()
        fig_pay = px.pie(pay_method, values='count', names='payment_method', hole=0.4)
        st.plotly_chart(fig_pay, use_container_width=True)

    # --- TAB 2: CLUSTERING INSIGHTS ---
    with tab2:
        st.header("Customer Segmentation Analysis")
        st.markdown("Detailed breakdown of machine-learning generated customer groups.")
        
        # --- 1. Cluster-Specific KPI Metrics ---
        # These metrics help stakeholders see the "Average Profile" of the filtered selection
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Avg Order Value", f"Rs. {df_selection['final_price'].mean():.2f}")
        with m2:
            st.metric("Avg Discount applied", f"{df_selection['discount_pct'].mean():.1f}%")
        with m3:
            st.metric("Most Active Cluster", f"C-{df_selection['cluster_id'].mode()[0]}")
        with m4:
            st.metric("Total Customers", len(df_selection['user_id'].unique()))

        st.divider()

        # --- 2. Cluster Visualization Grid ---
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Cluster Separation (ML Profile)")
            fig_scatter = px.scatter(
                df_selection, x="price", y="discount_pct", color="cluster_id", 
                title="Price vs Discount Sensitivity",
                labels={"price": "Unit Price", "discount_pct": "Discount %"}
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with c2:
            st.subheader("Revenue Contribution by Cluster")
            cluster_avg = df_selection.groupby('cluster_id')['final_price'].mean().reset_index()
            fig_cluster_bar = px.bar(
                cluster_avg, x='cluster_id', y='final_price', color='cluster_id',
                title="Avg Final Price per Cluster",
                text_auto='.2s'
            )
            st.plotly_chart(fig_cluster_bar, use_container_width=True)
            
        # --- 3. Heatmap and Time Series ---
        c3, c4 = st.columns(2)
        with c3:
            st.subheader("Cluster Category Affinity")
            heatmap_data = df_selection.groupby(['cluster_id', 'category']).size().reset_index(name='count')
            fig_heat = px.density_heatmap(
                heatmap_data, x="category", y="cluster_id", z="count", 
                color_continuous_scale="Viridis",
                title="Which groups buy what?"
            )
            st.plotly_chart(fig_heat, use_container_width=True)

        with c4:
            st.subheader("Sales Trend by Cluster")
            # Grouping by Month and Cluster for the trend line
            trend_data = df_selection.groupby([pd.Grouper(key='purchase_date', freq='M'), 'cluster_id'])['final_price'].sum().reset_index()
            fig_trend_cluster = px.line(
                trend_data, x="purchase_date", y="final_price", color="cluster_id",
                title="Revenue Evolution per Segment", 
                markers=True
            )
            st.plotly_chart(fig_trend_cluster, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")