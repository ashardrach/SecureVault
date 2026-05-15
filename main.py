import random
import string

# Generates a random password of the given length
def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ""
    for i in range(length):
        password = password + random.choice(characters)
    return password
#checks the strength of password
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
#saves password to text
def save_password(password):
    with open("passwords.txt", "a") as file:
        file.write(password + "\n")
#view password list
def view_passwords():
    print("\n--- Saved Passwords ---")
    try:
        with open("passwords.txt", "r") as file:
            passwords = file.readlines()
            if len(passwords) == 0:
                print("No passwords saved yet.")
            else:
                for i, password in enumerate(passwords):
                    print(str(i + 1) + ". " + password.strip())
    except FileNotFoundError:
        print("No passwords saved yet.")
    print("----------------------")

    
#controls everything
def main():
    print("Welcome to SecureVault")
    while True:
        print("\nWhat would you like to do?")
        print("1. Generate a password")
        print("2. View saved passwords")
        print("3. Exit")
        choice = input("Enter choice (1/2/3): ")

        if choice == "1":
            length = int(input("Enter password length: "))
            password = generate_password(length)
            print("Generated password:", password)
            strength = check_strength(password)
            print("Password strength:", strength)
            save_password(password)
            print("Password saved to passwords.txt")
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")

main()