from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RunModel(Base):
    __tablename__ = "runs"
    id = Column(String, primary_key=True, index=True)
    seed = Column(Integer, nullable=True)
    status = Column(String, default="IDLE")

class AnalysisModel(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String, index=True)
    gap_score = Column(Float)
    coverage_percentage = Column(Float)
    topic_similarity_score = Column(Float)
    result_json = Column(Text)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
