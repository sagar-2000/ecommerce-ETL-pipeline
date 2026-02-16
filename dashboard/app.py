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
    
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    return df

# 2. Page Configuration
st.set_page_config(page_title="E-commerce Cluster Insights", layout="wide")
st.title("E-commerce Customer Segmentation Dashboard")

try:
    df = get_data()

    # --- Sidebar Filters ---
    st.sidebar.header("Global Filters")
    category_list = df['category'].unique()
    selected_categories = st.sidebar.multiselect("Select Categories:", options=category_list, default=category_list)
    
    df_selection = df[df['category'].isin(selected_categories)]

    # --- Create Tabs ---
    tab1, tab2 = st.tabs(["General Business Insights", "Customer Segmentation"])

    # --- TAB 1: GENERAL INSIGHTS ---
    with tab1:
        st.header("General Business Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Which category is most bought over time?")
            category_trend = df_selection.groupby([pd.Grouper(key='purchase_date', freq='M'), 'category']).size().reset_index(name='units_sold')
            fig_trend = px.line(category_trend, x="purchase_date", y="units_sold", color="category", markers=True)
            st.plotly_chart(fig_trend, width="stretch")
            
        with col2:
            st.subheader("Which category generates the most revenue?")
            category_revenue = df_selection.groupby('category')['final_price'].sum().sort_values(ascending=False).reset_index()
            fig_rev = px.bar(category_revenue, x='category', y='final_price', color='final_price', color_continuous_scale='Greens')
            st.plotly_chart(fig_rev, width="stretch")

        st.divider()
        
        st.subheader("Preferred Payment Methods")
        pay_method = df_selection['payment_method'].value_counts().reset_index()
        fig_pay = px.pie(pay_method, values='count', names='payment_method', hole=0.4)
        st.plotly_chart(fig_pay, width="stretch")

    # --- TAB 2: CLUSTERING INSIGHTS ---
    with tab2:
        st.header("Customer Segmentation Analysis")
        
        df_selection['cluster_id'] = df_selection['cluster_id'].astype(str)
        
        unique_clusters = sorted(df_selection['cluster_id'].unique())
        colors = px.colors.qualitative.Plotly 
        color_map = {cluster: colors[i % len(colors)] for i, cluster in enumerate(unique_clusters)}

        # --- 2. Efficiency Analysis ---
        st.subheader("Efficiency Analysis: Revenue vs. Discount Sensitivity")
        
        eff_metrics = df_selection.groupby('cluster_id').agg({
            'final_price': 'sum',
            'discount_pct': 'mean',
            'user_id': 'count'
        }).reset_index()
        eff_metrics.columns = ['Cluster ID', 'Total Revenue', 'Avg Discount %', 'Order Count']
        eff_metrics['Efficiency Score'] = eff_metrics['Total Revenue'] / (eff_metrics['Avg Discount %'] + 1)
        eff_metrics = eff_metrics.sort_values(by='Efficiency Score', ascending=False)

        # --- STEP 2: STRATEGIC KPIs ---
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Revenue", f"Rs. {df_selection['final_price'].sum():,.0f}")
        with m2:
            top_efficiency = eff_metrics.iloc[0]['Cluster ID']
            st.metric("Most Efficient Segment", f"Cluster {top_efficiency}")
        with m3:
            avg_disc = eff_metrics[eff_metrics['Cluster ID'] == top_efficiency]['Avg Discount %'].values[0]
            st.metric(f"C-{top_efficiency} Avg Discount", f"{avg_disc:.1f}%")
        with m4:
            st.metric("Total Customer Base", f"{len(df_selection['user_id'].unique()):,}")

        st.divider()

        col_eff1, col_eff2 = st.columns([2, 1])

        with col_eff1:
            fig_bubble = px.scatter(
                eff_metrics, x="Avg Discount %", y="Total Revenue",
                size="Order Count", color="Cluster ID", text="Cluster ID",
                color_discrete_map=color_map,
                title="Strategic Mapping: Revenue vs. Discount Sensitivity"
            )
            st.plotly_chart(fig_bubble, width="stretch")

        with col_eff2:
            st.write("**Revenue Efficiency Leaderboard**")
            st.dataframe(eff_metrics[['Cluster ID', 'Total Revenue', 'Efficiency Score']], 
                         hide_index=True, width="stretch")
            st.success(f"Cluster {eff_metrics.iloc[0]['Cluster ID']} is the winner!")

        st.divider()

        # --- 3. Cluster Visualization Grid ---
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Cluster Separation (ML Profile)")
            fig_scatter = px.scatter(
                df_selection, x="price", y="discount_pct", color="cluster_id", 
                color_discrete_map=color_map,
                title="Price vs Discount Sensitivity"
            )
            st.plotly_chart(fig_scatter, width="stretch")
        
        with c2:
            st.subheader("Revenue Contribution by Cluster")
            cluster_rev = df_selection.groupby('cluster_id')['final_price'].sum().reset_index()
            fig_cluster_bar = px.bar(
                cluster_rev, x='cluster_id', y='final_price', color='cluster_id',
                color_discrete_map=color_map,
                title="Total Revenue per Cluster",
                text_auto='.2s'
            )
            fig_cluster_bar.update_layout(xaxis={'categoryorder':'array', 'categoryarray':unique_clusters})
            st.plotly_chart(fig_cluster_bar, width="stretch")
            
        # --- 4. Heatmap and Time Series ---
        c3, c4 = st.columns(2)
        with c3:
            st.subheader("Cluster Category Affinity")
            heatmap_data = df_selection.groupby(['cluster_id', 'category']).size().reset_index(name='count')
            fig_heat = px.density_heatmap(
                heatmap_data, x="category", y="cluster_id", z="count", 
                color_continuous_scale="Viridis", text_auto=True,
                title="Who buys what? (Order Density)"
            )
            fig_heat.update_layout(yaxis={'type': 'category', 'categoryorder':'array', 'categoryarray':unique_clusters})
            st.plotly_chart(fig_heat, width="stretch", theme=None)

        with c4:
            st.subheader("Sales Trend by Cluster")
            trend_data = df_selection.groupby([pd.Grouper(key='purchase_date', freq='M'), 'cluster_id'])['final_price'].sum().reset_index()
            fig_trend_cluster = px.line(
                trend_data, x="purchase_date", y="final_price", color="cluster_id",
                color_discrete_map=color_map,
                title="Revenue Evolution per Segment", markers=True
            )
            st.plotly_chart(fig_trend_cluster, width="stretch")

except Exception as e:
    st.error(f"Error: {e}")