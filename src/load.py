from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def load_to_postgres(df):
    user = os.getenv("DB_USER")
    pw = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")
    
    engine = create_engine(f'postgresql://{user}:{pw}@{host}:{port}/{db}')
    
    # Using 'replace' for the first run to create the table automatically
    df.to_sql('ecommerce_sales', engine, if_exists='replace', index=False, chunksize=1000)
    print("Successfully loaded data to PostgreSQL!")