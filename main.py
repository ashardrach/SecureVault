import random
import string
import os
import hashlib
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

# ─── Encryption ───────────────────────────────────────────

def load_key():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as file:
            return file.read()
    else:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as file:
            file.write(key)
        return key

def encrypt(text, key):
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()

def decrypt(text, key):
    f = Fernet(key)
    return f.decrypt(text.encode()).decode()

# ─── Master Password ──────────────────────────────────────

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_master(password):
    with open("master.hash", "w") as file:
        file.write(hash_password(password))

def load_master():
    if os.path.exists("master.hash"):
        with open("master.hash", "r") as file:
            return file.read()
    return None

def verify_master(password):
    stored_hash = load_master()
    if stored_hash is None:
        return False
    return hash_password(password) == stored_hash

# ─── Password Logic ───────────────────────────────────────

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ""
    for i in range(length):
        password = password + random.choice(characters)
    return password

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

def save_password(label, password, key):
    encrypted = encrypt(password, key)
    with open("passwords.csv", "a") as file:
        file.write(label.strip() + "," + encrypted + "\n")

def load_passwords(key):
    passwords = []
    if not os.path.exists("passwords.csv"):
        return passwords
    with open("passwords.csv", "r") as file:
        lines = file.readlines()
    for line in lines:
        parts = line.strip().split(",")
        if len(parts) == 2:
            label = parts[0]
            password = decrypt(parts[1], key)
            passwords.append((label, password))
    return passwords

def delete_password_by_label(keyword, key):
    if not os.path.exists("passwords.csv"):
        return 0
    with open("passwords.csv", "r") as file:
        lines = file.readlines()
    updated = []
    deleted = 0
    for line in lines:
        parts = line.strip().split(",")
        if parts[0].lower() != keyword.lower():
            updated.append(line)
        else:
            deleted = deleted + 1
    with open("passwords.csv", "w") as file:
        file.writelines(updated)
    return deleted

# ─── Login Screen ─────────────────────────────────────────

class LoginScreen:

    def __init__(self, root, key):
        self.root = root
        self.key = key
        self.root.title("SecureVault — Login")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")
        self.build_ui()

    def build_ui(self):
        tk.Label(
            self.root,
            text="SecureVault 🔐",
            font=("Helvetica", 22, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4"
        ).pack(pady=30)

        existing = load_master()

        if existing is None:
            tk.Label(
                self.root,
                text="Welcome! Set your master password:",
                font=("Helvetica", 11),
                bg="#1e1e2e",
                fg="#a6e3a1"
            ).pack(pady=5)
        else:
            tk.Label(
                self.root,
                text="Enter your master password:",
                font=("Helvetica", 11),
                bg="#1e1e2e",
                fg="#cdd6f4"
            ).pack(pady=5)

        self.password_entry = tk.Entry(
            self.root,
            width=25,
            font=("Helvetica", 13),
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="white",
            relief="flat",
            show="•"
        )
        self.password_entry.pack(pady=10)
        self.password_entry.focus()
        self.password_entry.bind("<Return>", lambda e: self.submit())

        if existing is None:
            tk.Label(
                self.root,
                text="Confirm master password:",
                font=("Helvetica", 11),
                bg="#1e1e2e",
                fg="#cdd6f4"
            ).pack(pady=5)

            self.confirm_entry = tk.Entry(
                self.root,
                width=25,
                font=("Helvetica", 13),
                bg="#313244",
                fg="#cdd6f4",
                insertbackground="white",
                relief="flat",
                show="•"
            )
            self.confirm_entry.pack(pady=5)
        else:
            self.confirm_entry = None

        btn_text = "Set Password" if existing is None else "Unlock Vault"

        tk.Button(
            self.root,
            text=btn_text,
            command=self.submit,
            bg="#89b4fa",
            fg="#1e1e2e",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=20)

        self.error_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 10),
            bg="#1e1e2e",
            fg="#f38ba8"
        )
        self.error_label.pack()

    def submit(self):
        password = self.password_entry.get()

        if password == "":
            self.error_label.config(text="Please enter a password.")
            return

        existing = load_master()

        if existing is None:
            confirm = self.confirm_entry.get()
            if password != confirm:
                self.error_label.config(text="Passwords do not match.")
                return
            if len(password) < 6:
                self.error_label.config(
                    text="Master password must be at least 6 characters.")
                return
            save_master(password)
            self.open_vault()
        else:
            if verify_master(password):
                self.open_vault()
            else:
                self.error_label.config(text="Incorrect password. Try again.")

    def open_vault(self):
        self.root.destroy()
        new_root = tk.Tk()
        SecureVaultApp(new_root, self.key)
        new_root.mainloop()

# ─── Main Vault App ───────────────────────────────────────

class SecureVaultApp:

    def __init__(self, root, key):
        self.root = root
        self.key = key
        self.root.title("SecureVault")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")
        self.build_ui()

    def build_ui(self):
        tk.Label(
            self.root,
            text="SecureVault 🔐",
            font=("Helvetica", 20, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4"
        ).pack(pady=20)

        input_frame = tk.Frame(self.root, bg="#1e1e2e")
        input_frame.pack(pady=5)

        tk.Label(
            input_frame,
            text="Label (e.g. Gmail):",
            bg="#1e1e2e",
            fg="#cdd6f4",
            font=("Helvetica", 11)
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

        self.label_entry = tk.Entry(
            input_frame,
            width=25,
            font=("Helvetica", 11),
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="white",
            relief="flat"
        )
        self.label_entry.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(
            input_frame,
            text="Password Length:",
            bg="#1e1e2e",
            fg="#cdd6f4",
            font=("Helvetica", 11)
        ).grid(row=1, column=0, padx=10, pady=8, sticky="w")

        self.length_entry = tk.Entry(
            input_frame,
            width=25,
            font=("Helvetica", 11),
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="white",
            relief="flat"
        )
        self.length_entry.insert(0, "16")
        self.length_entry.grid(row=1, column=1, padx=10, pady=8)

        tk.Button(
            self.root,
            text="Generate Password",
            command=self.generate,
            bg="#89b4fa",
            fg="#1e1e2e",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=10)

        self.password_var = tk.StringVar()
        self.password_var.set("Your password will appear here")

        tk.Label(
            self.root,
            textvariable=self.password_var,
            font=("Courier", 13, "bold"),
            bg="#313244",
            fg="#a6e3a1",
            pady=12,
            padx=20,
            wraplength=440
        ).pack(fill="x", padx=30, pady=5)

        self.strength_var = tk.StringVar()
        self.strength_var.set("")

        tk.Label(
            self.root,
            textvariable=self.strength_var,
            font=("Helvetica", 10),
            bg="#1e1e2e",
            fg="#f9e2af"
        ).pack()

        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="💾 Save Password",
            command=self.save,
            bg="#a6e3a1",
            fg="#1e1e2e",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            padx=15,
            pady=6,
            cursor="hand2"
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            btn_frame,
            text="📋 Copy Password",
            command=self.copy,
            bg="#89dceb",
            fg="#1e1e2e",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            padx=15,
            pady=6,
            cursor="hand2"
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            btn_frame,
            text="🗑 Delete by Label",
            command=self.delete,
            bg="#f38ba8",
            fg="#1e1e2e",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            padx=15,
            pady=6,
            cursor="hand2"
        ).grid(row=0, column=2, padx=8)

        search_frame = tk.Frame(self.root, bg="#1e1e2e")
        search_frame.pack(pady=5)

        self.search_entry = tk.Entry(
            search_frame,
            width=25,
            font=("Helvetica", 11),
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="white",
            relief="flat"
        )
        self.search_entry.insert(0, "Search by label...")
        self.search_entry.grid(row=0, column=0, padx=8)

        tk.Button(
            search_frame,
            text="Search",
            command=self.search,
            bg="#cba6f7",
            fg="#1e1e2e",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2"
        ).grid(row=0, column=1, padx=8)

        tk.Label(
            self.root,
            text="Saved Passwords",
            font=("Helvetica", 11, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4"
        ).pack(pady=(15, 5))

        self.listbox = tk.Listbox(
            self.root,
            width=60,
            height=8,
            font=("Courier", 10),
            bg="#313244",
            fg="#cdd6f4",
            selectbackground="#89b4fa",
            relief="flat",
            borderwidth=0
        )
        self.listbox.pack(padx=30)
        self.refresh_list()

    def generate(self):
        try:
            length = int(self.length_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for length.")
            return
        password = generate_password(length)
        strength = check_strength(password)
        self.password_var.set(password)
        self.strength_var.set("Strength: " + strength)

    def save(self):
        label = self.label_entry.get().strip()
        password = self.password_var.get()
        if label == "":
            messagebox.showerror("Error", "Please enter a label.")
            return
        if password == "Your password will appear here":
            messagebox.showerror("Error", "Please generate a password first.")
            return
        save_password(label, password, self.key)
        self.refresh_list()
        messagebox.showinfo("Saved", "Password saved for: " + label)

    def copy(self):
        password = self.password_var.get()
        if password == "Your password will appear here":
            messagebox.showerror("Error", "No password to copy.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard.")

    def delete(self):
        label = self.label_entry.get().strip()
        if label == "":
            messagebox.showerror("Error", "Enter a label to delete.")
            return
        deleted = delete_password_by_label(label, self.key)
        if deleted > 0:
            messagebox.showinfo("Deleted", "Deleted password for: " + label)
        else:
            messagebox.showerror("Not Found", "No password found for: " + label)
        self.refresh_list()

    def search(self):
        keyword = self.search_entry.get().strip().lower()
        passwords = load_passwords(self.key)
        self.listbox.delete(0, tk.END)
        for label, password in passwords:
            if keyword in label.lower():
                self.listbox.insert(tk.END, label + "  ->  " + password)

    def refresh_list(self):
        passwords = load_passwords(self.key)
        self.listbox.delete(0, tk.END)
        for label, password in passwords:
            self.listbox.insert(tk.END, label + "  ->  " + password)

# ─── Start ────────────────────────────────────────────────

key = load_key()
root = tk.Tk()
app = LoginScreen(root, key)
root.mainloop()