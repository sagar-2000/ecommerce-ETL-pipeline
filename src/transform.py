import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def apply_clustering(df, n_clusters=7):
    print("--- Starting Transformation & Clustering ---")
    
    df = df.rename(columns={
        'User_ID': 'user_id',
        'Product_ID': 'product_id',
        'Category': 'category',
        'Price (Rs.)': 'price',
        'Discount (%)': 'discount_pct',
        'Final_Price(Rs.)': 'final_price',
        'Payment_Method': 'payment_method',
        'Purchase_Date': 'purchase_date'
    })
    
    # 1. Cleaning & Feature Selection
    # (Ensure names are lowercase/underscored for PostgreSQL compatibility)
    df_ml = df[['price', 'discount_pct', 'final_price']].copy()
    
    # 2. Scaling
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df_ml)
    
    # 3. Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['cluster_id'] = kmeans.fit_predict(scaled_data)
    
    # 4. Date conversion
    df['purchase_date'] = pd.to_datetime(df['purchase_date'], dayfirst=True)
    
    print(f"Clustering complete. Identified {n_clusters} customer segments.")
    return df