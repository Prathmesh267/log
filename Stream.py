import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
import mysql.connector

# MySQL connection parameters
DATABASE_USERNAME = 'root'
DATABASE_PASSWORD = '12345'
DATABASE_HOST = 'localhost'  # or the address of your MySQL server
DATABASE_NAME = 'UserData'

# Create a connection to the MySQL database
engine = create_engine(f'mysql+mysqlconnector://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}')
metadata = MetaData()

# Define the 'users' table structure
users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('username', String, unique=True),
                    Column('password', String),
                    Column('email', String, unique=True))

# Create the table in the MySQL database
metadata.create_all(engine)

# Create a session for DB transactions
Session = sessionmaker(bind=engine)
session = Session()

# Function to check if the user already exists by username or email
def user_exists(username, email):
    stmt = select([users_table]).where((users_table.c.username == username) | (users_table.c.email == email))
    result = session.execute(stmt).fetchone()
    return result is not None

# Function to create a new user
def create_user(username, password, email):
    if not user_exists(username, email):  # Check if the user already exists
        new_user = {'username': username, 'password': password, 'email': email}
        ins = users_table.insert().values(new_user)
        session.execute(ins)
        session.commit()
        return True
    return False  # User already exists

# Function to validate login credentials
def check_user(username, password):
    stmt = select([users_table]).where(users_table.c.username == username)
    user = session.execute(stmt).fetchone()
    if user and user.password == password:
        return True
    return False

# Streamlit function for sign-up page
def sign_up():
    st.title("Sign Up")
    username = st.text_input("Enter your username")
    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type='password')
    
    if st.button("Sign Up"):
        if create_user(username, password, email):
            st.success("User registered successfully!")
        else:
            st.error("User already exists. Try with a different username or email!")

# Streamlit function for login page
def login():
    st.title("Login")
    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type='password')
    
    if st.button("Login"):
        if check_user(username, password):
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

# Main Streamlit function
def main():
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Sign Up":
        sign_up()
    elif choice == "Login":
        login()

if __name__ == '__main__':
    main()
