from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import SQLModel, create_engine

# import warnings
# warnings.simplefilter(action="ignore", category=UserWarning)


class Settings(BaseSettings):
    frontend_url: str = "http://localhost:8001"

    db_user: str = "luce"
    db_password: str = "luce123456"
    db_host: str = "postgres_db"
    db_name: str = "lucedb"

    admin_email: str = "admin@example.com"
    admin_password: str = "changeme"

    # redirect_uri: str = "http://localhost:3000/cb"
    # auth_endpoint: str = ""
    # client_id: str = ""
    # client_secret: str = ""
    # response_type: str = "code"
    # scope: str = "email"

    # data_folder: str = "../data/cohorts"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @computed_field()
    def db_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:5432/{self.db_name}"


settings = Settings()


engine = create_engine(
    settings.db_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)
# Use echo=True to see the details of all SQL transactions done by SQLalchemy


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
