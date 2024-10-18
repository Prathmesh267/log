import sqlite3

from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
import sqlite3

# Create an SQLite database
engine = create_engine('sqlite:///UserData.db')  # You can replace with another DB if needed
metadata = MetaData()

# Define the table
users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('username', String, unique=True),
                    Column('password', String),
                    Column('email', String))

# Create the table in the database
metadata.create_all(engine)

# Creating a session for DB transactions
Session = sessionmaker(bind=engine)
session = Session()
