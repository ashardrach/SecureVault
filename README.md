# SecureVault 🔐

A command-line password generator and manager built in Python.

## Features
- Generate strong random passwords
- Check password strength (Weak / Medium / Strong / Very Strong)
- Label passwords by service (Gmail, GitHub, etc.)
- Save passwords with Fernet encryption
- View all saved passwords
- Search passwords by label
- Delete passwords by label
- Full GUI with dark theme built with Tkinter


## Security
- Passwords are encrypted using Fernet symmetric encryption
- Encryption key stored locally in secret.key
- passwords.csv and secret.key are excluded from version control

## How to Run
1. Make sure Python is installed
2. Clone this repository:
   git clone https://github.com/ashardrach/SecureVault.git
3. Install the required library:
   pip install cryptography
4. Run the program:
   python main.py

## Project Structure
main.py        → main program
passwords.csv  → encrypted password storage (not uploaded)
secret.key     → encryption key (not uploaded)
.gitignore     → protects sensitive files

## What I Learned
- Python fundamentals (variables, loops, functions)
- File handling and CSV data storage
- Fernet encryption and cybersecurity basics
- Error handling and input validation
- Git and GitHub workflow
- Code organization and documentation




## How to Run
1. Make sure Python is installed
2. Clone this repository:
   git clone https://github.com/ashardrach/SecureVault.git
3. Install the required library:
   pip install cryptography
4. Run the program:
   python main.py
5. A window will open — no terminal needed



## Built By
ashardrach — cybersecurity student learning Python by building real tools.