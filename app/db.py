from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError 
from .config import Settings

settings = Settings()

host = settings.host
user = settings.database_username
password = settings.database_password
port = settings.port
database_name = settings.database_name

POSTGRES_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database_name}"

def create_database_if_not_exists():
    try:
        temp_engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/postgres")
        with temp_engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT")
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{database_name}'"))
            if not result.fetchone():
                conn.execute(text(f"CREATE DATABASE {database_name}"))
                print(f"Database '{database_name}' created successfully")
            else:
                print(f"Database '{database_name}' already exists")
        temp_engine.dispose()
    except Exception as e:
        print(f"Error creating database: {e}")

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
        print("Database session created")
    finally:
        db.close()
