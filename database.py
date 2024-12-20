from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

print("DATABASE_URL:")
print(os.getenv("DATABASE_URL"))
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DBIngredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    amount = Column(Float)
    unit = Column(String)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))

class DBRecipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    instructions = Column(JSON)
    ingredients = relationship("DBIngredient", cascade="all, delete-orphan")

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
