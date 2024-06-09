from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv


# Load environment variables from a .env file
load_dotenv()

# Get the database URL from the environment variables
URL_DATABASE = os.getenv("URL_DATABASE")

# Create the SQLAlchemy engine
engine = create_engine(URL_DATABASE,echo=True)

# Create a configured "Session" class
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our classes definitions
base = declarative_base()