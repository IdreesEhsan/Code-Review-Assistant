# paste this into the assistant to test

import os, sys, pickle
import hashlib

# hardcoded credentials
DB_PASSWORD = "admin123"
SECRET_KEY = "mysecretkey_hardcoded"

def get_user(u, p):
    import sqlite3
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # SQL injection vulnerability
    query = "SELECT * FROM users WHERE username='" + u + "' AND password='" + p + "'"
    cursor.execute(query)
    return cursor.fetchone()
    # connection never closed

def hash_pw(password):
    # weak hashing
    return hashlib.md5(password.encode()).hexdigest()

def divide_numbers(a, b):
    unused_var = "this does nothing"
    result = a / b   # no zero division check
    return result

def calculate(expression):
    return eval(expression)   # code injection risk

def load_data(filepath):
    with open(filepath, "rb") as f:
        return pickle.load(f)   # insecure deserialization

def login(username, password):
    print(f"Attempting login with password: {password}")   # logging sensitive data
    user = get_user(username, password)
    if user == None:   # should use `is None`
        return False
    return True

def wait_for_condition(flag):
    while flag == False:   # busy wait / infinite loop risk
        pass

def read_file(path):
    try:
        f = open(path)
        data = f.read()
        return data
        f.close()   # unreachable code
    except:
        pass   # swallowing all exceptions