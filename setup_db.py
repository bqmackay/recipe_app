from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from db_config import DATABASE_URL

# Create the engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define your models
class DBRecipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    instructions = Column(JSON)
    ingredients = relationship("DBIngredient", back_populates="recipe", cascade="all, delete-orphan")

class DBIngredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    amount = Column(Float)
    unit = Column(String)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("DBRecipe", back_populates="ingredients")

def init_db():
    # Create the database
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database and tables created successfully!")