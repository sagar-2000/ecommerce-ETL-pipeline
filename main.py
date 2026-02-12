import logging
from src.extract import extract_data
from src.transform import apply_clustering
from src.load import load_to_postgres

# Professional touch: Logging tracks what happened and when
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    try:
        logging.info("Pipeline Started.")
        
        # 1. EXTRACT
        df = extract_data()
        
        # 2. TRANSFORM
        clusters_to_find = 7 
        df_clustered = apply_clustering(df, n_clusters=clusters_to_find)
        
        # 3. LOAD
        load_to_postgres(df_clustered)
        
        logging.info("Pipeline completed successfully.")
        
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    run_pipeline()