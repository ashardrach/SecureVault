import random
import string
import os
from cryptography.fernet import Fernet

# Generates a random password of the given length
def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ""
    for i in range(length):
        password = password + random.choice(characters)
    return password

# Checks the strength of a password
def check_strength(password):
    score = 0
    if len(password) >= 8:
        score = score + 1
    if any(c.isupper() for c in password):
        score = score + 1
    if any(c.islower() for c in password):
        score = score + 1
    if any(c.isdigit() for c in password):
        score = score + 1
    if any(c in string.punctuation for c in password):
        score = score + 1
    if score == 5:
        return "Very Strong"
    elif score == 4:
        return "Strong"
    elif score == 3:
        return "Medium"
    else:
        return "Weak"

# Loads existing key or creates a new one
def load_key():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as file:
            return file.read()
    else:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as file:
            file.write(key)
        return key

# Encrypts text using the key
def encrypt(text, key):
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()

# Decrypts text using the key
def decrypt(text, key):
    f = Fernet(key)
    return f.decrypt(text.encode()).decode()

# Saves a labeled password to the csv file
def save_password(label, password, key):
    encrypted_password = encrypt(password, key)
    with open("passwords.csv", "a") as file:
        file.write(label.strip() + "," + encrypted_password + "\n")

# Displays all saved passwords
def view_passwords(key):
    print("\n--- Saved Passwords ---")
    try:
        with open("passwords.csv", "r") as file:
            passwords = file.readlines()
            if len(passwords) == 0:
                print("No passwords saved yet.")
            else:
                for i, line in enumerate(passwords):
                    parts = line.strip().split(",")
                    label = parts[0]
                    encrypted_password = parts[1]
                    password = decrypt(encrypted_password, key)
                    print(str(i + 1) + ". " + label + " -> " + password)
    except FileNotFoundError:
        print("No passwords saved yet.")
    print("----------------------")

# Searches passwords by label
def search_password(keyword, key):
    print("\n--- Search Results ---")
    try:
        with open("passwords.csv", "r") as file:
            passwords = file.readlines()
            found = 0
            for line in passwords:
                parts = line.strip().split(",")
                label = parts[0]
                encrypted_password = parts[1]
                if keyword.lower() in label.lower():
                    password = decrypt(encrypted_password, key)
                    print(label + " -> " + password)
                    found = found + 1
            if found == 0:
                print("No matches found for: " + keyword)
    except FileNotFoundError:
        print("No passwords saved yet.")
    print("----------------------")

# Deletes a password by label
def delete_password(keyword):
    try:
        with open("passwords.csv", "r") as file:
            passwords = file.readlines()

        updated = []
        deleted = 0
        for line in passwords:
            parts = line.strip().split(",")
            label = parts[0]
            if keyword.lower() != label.lower():
                updated.append(line)
            else:
                deleted = deleted + 1

        with open("passwords.csv", "w") as file:
            file.writelines(updated)

        if deleted > 0:
            print("Password for " + keyword + " deleted successfully.")
        else:
            print("No password found with label: " + keyword)

    except FileNotFoundError:
        print("No passwords saved yet.")

# Controls everything
def main():
    key = load_key()
    print("Welcome to SecureVault")
    while True:
        print("\nWhat would you like to do?")
        print("1. Generate a password")
        print("2. View saved passwords")
        print("3. Search passwords")
        print("4. Delete a password")
        print("5. Exit")
        choice = input("Enter choice (1/2/3/4/5): ")

        if choice == "1":
            label = input("Enter label (e.g. Gmail, GitHub): ")
            length = int(input("Enter password length: "))
            password = generate_password(length)
            print("Generated password:", password)
            strength = check_strength(password)
            print("Password strength:", strength)
            save_password(label, password, key)
            print("Password saved successfully.")
        elif choice == "2":
            view_passwords(key)
        elif choice == "3":
            keyword = input("Enter label to search: ")
            search_password(keyword, key)
        elif choice == "4":
            keyword = input("Enter label to delete: ")
            delete_password(keyword)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4 or 5.")

main()