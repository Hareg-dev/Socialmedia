from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    host: str = "localhost"
    port: str = "5432"
    database_name: str = "fastapi-cource"
    database_password: str = ""
    database_username: str = "postgres"
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

    @property
    def DATABASE_URL(self):
        return f"postgresql+psycopg2://{self.database_username}:{self.database_password}@{self.host}:{self.port}/{self.database_name}"