from sqlmodel import SQLModel, create_engine
from sqlalchemy import inspect, text
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, engine_uri: str):
        connection_args = {"check_same_thread": False} if "sqlite" in engine_uri else {}
        self.engine = create_engine(engine_uri, connect_args=connection_args)

    def initialize_database(self):
        try:
            # Enable foreign key constraints for SQLite
            if "sqlite" in str(self.engine.url):
                with self.engine.connect() as conn:
                    conn.execute(text("PRAGMA foreign_keys=ON"))

            inspector = inspect(self.engine)
            tables_exist = inspector.get_table_names()
            if not tables_exist:
                logger.info("Creating database tables...")
                # We need to import the Student model here so that SQLModel knows about it
                from models import Student
                SQLModel.metadata.create_all(self.engine)
                logger.info("Database tables created successfully.")
            else:
                logger.info("Database tables already exist.")

        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")

# Global instance
DATABASE_URL = "sqlite:///database.db"
db_manager = DatabaseManager(DATABASE_URL)

def get_session():
    from sqlmodel import Session
    with Session(db_manager.engine) as session:
        yield session
