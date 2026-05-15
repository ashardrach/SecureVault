# SecureVault 🔐

A secure desktop password manager built in Python with a full GUI.

## Features
- Master password login (SHA256 hashed — never stored in plain text)
- Generate strong random passwords
- Check password strength (Weak / Medium / Strong / Very Strong)
- Label passwords by service (Gmail, GitHub, etc.)
- Fernet encryption on all stored passwords
- View, search and delete saved passwords
- Professional dark theme GUI built with Tkinter

## Security Design
- Master password is hashed with SHA256 — never stored raw
- Passwords encrypted with Fernet symmetric encryption
- Encryption key stored locally in secret.key
- Sensitive files excluded from version control via .gitignore

## How to Run
1. Make sure Python is installed
2. Clone this repository:
   git clone https://github.com/ashardrach/SecureVault.git
3. Install required library:
   pip install cryptography
4. Run the program:
   python main.py
5. Set your master password on first run
6. Vault opens after successful login

## Project Structure
main.py       → full application code
.gitignore    → protects sensitive files

## Skills Demonstrated
- Python (functions, loops, file handling, OOP basics)
- Cryptography (Fernet encryption, SHA256 hashing)
- GUI development (Tkinter)
- Secure coding practices
- Git and GitHub version control

## Built By
ashardrach — cybersecurity student building real tools.
GitHub: github.com/ashardrach