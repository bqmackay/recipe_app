import os
from dotenv import load_dotenv

load_dotenv()

# Create the database URL
DATABASE_URL = os.getenv("DATABASE_URL")

print(DATABASE_URL)