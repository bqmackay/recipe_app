# Database URL - modify these values according to your setup
DB_USER = "postgres"
DB_PASSWORD = "postgres"  # Change this to your password
DB_NAME = "recipe_db"
DB_HOST = "localhost"

# Create the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"