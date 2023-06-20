from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from habit import Base

# Get the current directory
current_directory = os.getcwd()

# Construct the file path for the database
database_file = "habits.db"
database_path = os.path.join(current_directory, database_file)

# create the engine: sqlite
engine = create_engine(f"sqlite:///{database_path}")
Base.metadata.create_all(engine)

# connect to the database to execute sql statements
Session = sessionmaker(bind=engine)
session = Session()
