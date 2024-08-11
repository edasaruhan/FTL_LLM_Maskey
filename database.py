from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./FTL_LLM.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class TextSummary(Base):
    """
    SQLAlchemy model for storing text summaries and extracted entities.

    Attributes:
        id (int): Primary key, auto-incremented.
        original_text (str): The original text input.
        summary (str): The summary generated from the original text.
        entities (str): The named entities extracted from the original text.
    """
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    entities = Column(Text, nullable=False)

def init_db():
    """
    Initializes the database by creating all tables defined in the Base metadata.

    This function should be called when the application starts to ensure that the 
    database schema is in place. It creates the tables in the database if they do 
    not already exist.
    """
    Base.metadata.create_all(bind=engine)
