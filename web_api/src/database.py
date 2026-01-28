"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import current_config
from logger import app_logger

DATABASE_URL = f"sqlite:///{current_config.DATABASE}"

# Create engine with SQLite specific settings
engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False}
)

db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """
    Initialize the database and create tables
    """
    try:
        import models  # noqa: F401 - Import to register models
        Base.metadata.create_all(bind=engine)
        app_logger.info("Database initialized successfully")
    except Exception as e:
        app_logger.error(f"Error initializing database: {str(e)}")
        raise


def close_db_session():
    """
    Close database session
    """
    db_session.remove()

