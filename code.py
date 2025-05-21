import tkinter as tk
import re

def check_strength(password):
    score = 0
    length = len(password)

    if length >= 6:
        score += 1
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    if length == 0:
        return "Empty"
    elif score == 1:
        return "Extremely Weak"
    elif score == 2:
        return "Very Weak"
    elif score == 3:
        return "Weak"
    elif score == 4:
        return "Fair"
    elif score == 5:
        return "Good"
    elif score == 6:
        return "Strong"
    else:
        return "Very Strong"

# UI Setup
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("400x200")
root.configure(bg="#f2f2f2")

def on_check():
    pw = entry.get()
    result = check_strength(pw)
    output.config(text="Strength: " + result)

title = tk.Label(root, text="Password Strength Checker", font=("Arial", 16, "bold"), bg="#f2f2f2")
title.pack(pady=10)

entry = tk.Entry(root, show="*", font=("Arial", 14), width=30)
entry.pack()

check_button = tk.Button(root, text="Check", command=on_check, font=("Arial", 12), bg="#4CAF50", fg="white")
check_button.pack(pady=10)

output = tk.Label(root, text="", font=("Arial", 14), bg="#f2f2f2")
output.pack()

root.mainloop()