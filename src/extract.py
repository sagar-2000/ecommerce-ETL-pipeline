import kagglehub
from kagglehub import KaggleDatasetAdapter

def extract_data():
    print("--- Starting Extraction ---")
    file_path = "ecommerce_dataset_updated.csv"
    
    df = kagglehub.load_dataset(
      KaggleDatasetAdapter.PANDAS,
      "steve1215rogg/e-commerce-dataset",
      file_path,
    )
    print(f"Successfully extracted {len(df)} rows.")
    return df