import hashlib
import json
import os

USER_FILE = "users.json"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    if not os.path.exists(USER_FILE):
        return {}

    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


def register_user(username, password):
    users = load_users()

    if username in users:
        return False, "User already exists"

    users[username] = hash_password(password)
    save_users(users)

    return True, "Registration successful"


def login_user(username, password):
    users = load_users()

    if username not in users:
        return False, "User not found"

    if users[username] == hash_password(password):
        return True, "Login successful"

    return False, "Incorrect password"
