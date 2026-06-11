from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


def _resolve_database_url() -> str:
    explicit = os.getenv("DATABASE_URL")
    if explicit:
        return explicit
    if os.getenv("DB_HOST"):
        from core.config import settings

        return (
            f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}"
            f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        )
    return "sqlite:///./dev.db"


DATABASE_URL = _resolve_database_url()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    from modulos.delivery.infrastructure.models import Base as DeliveryBase
    DeliveryBase.metadata.create_all(bind=engine)
