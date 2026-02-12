import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv() # Loads variables from .env

def get_engine():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")
    
    # SQLAlchemy connection string for PostgreSQL
    conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    return create_engine(conn_str)