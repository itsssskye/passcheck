import tkinter as tk
import re

# Scoring and return system
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

# Strength Colors
def get_color_for_strength(strength):
    colors = {
        "Empty": "#000000",              # Black
        "Extremely Weak": "#ff0000",     # Red
        "Very Weak": "#ff5500",          # Red-Orange
        "Weak": "#ff9900",               # Orange
        "Fair": "#ffcc00",               # Yellow
        "Good": "#aacc00",               # Yellow-Green
        "Strong": "#66cc00",             # Greenish
        "Very Strong": "#00cc00",        # Green
    }
    return colors.get(strength, "#000000")

# Key Input
def on_key_release(event=None):
    pw = entry.get()
    result = check_strength(pw)
    color = get_color_for_strength(result)
    output.config(text="Strength: " + result, fg=color)

# UI Setup
root = tk.Tk()
root.title("PassCheck")
root.configure(bg="#f2f2f2")

# Center
window_width = 400
window_height = 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Title
title = tk.Label(root, text="PassCheck", font=("Arial", 18, "bold"), bg="#f2f2f2")
title.pack(pady=(20, 10))

# Entry
entry = tk.Entry(root, show="*", font=("Arial", 14), width=30, justify="center")
entry.pack(pady=5)
entry.focus()
entry.bind("<KeyRelease>", on_key_release)

# Output Label
output = tk.Label(root, text="", font=("Arial", 14), bg="#f2f2f2")
output.config(text="Strength: Empty", fg="#000000")
output.pack(pady=10)

root.mainloop()