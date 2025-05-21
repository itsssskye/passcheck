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
        return "Empty", 0
    elif score == 1:
        return "Extremely Weak", 1
    elif score == 2:
        return "Very Weak", 2
    elif score == 3:
        return "Weak", 3
    elif score == 4:
        return "Fair", 4
    elif score == 5:
        return "Good", 5
    elif score == 6:
        return "Strong", 6
    elif score >= 7:
        return "Extremely Strong", 7
    else:
        return "Very Strong", 6  # fallback

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
        "Extremely Strong": "#00ff00",  # Bright Green
    }
    return colors.get(strength, "#000000")

# On key release update label and progress bar
def on_key_release(event=None):
    pw = entry.get()
    result, score = check_strength(pw)
    color = get_color_for_strength(result)
    output.config(text="Strength: " + result, fg=color)

    # Update progress bar fill length (max score = 7)
    max_score = 7
    bar_width = 300
    fill_width = int((score / max_score) * bar_width)
    
    # Clear previous bar
    canvas.delete("bar_fill")
    
    # Draw filled part of bar
    if fill_width > 0:
        canvas.create_rectangle(0, 0, fill_width, 20, fill="#ffffff", tags="bar_fill")
    
    # Draw colored overlay for strength
    if fill_width > 0:
        canvas.create_rectangle(0, 0, fill_width, 20, fill=color, tags="bar_fill_overlay")
    else:
        # No fill if empty password
        pass

# UI Setup
root = tk.Tk()
root.title("PassCheck")
root.configure(bg="#a0c8f0")  # Soft pastel blue background

# Center
window_width = 400
window_height = 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Title
title = tk.Label(root, text="PassCheck", font=("Segoe UI", 22, "bold"), bg="#a0c8f0", fg="#0a1f44")
title.pack(pady=(20, 10))

# Entry
entry = tk.Entry(root, show="*", font=("Segoe UI", 16), width=30, justify="center")
entry.pack(pady=5)
entry.focus()
entry.bind("<KeyRelease>", on_key_release)

# Output Label
output = tk.Label(root, text="", font=("Segoe UI", 16, "bold"), bg="#a0c8f0")
output.pack(pady=10)

# Canvas for progress bar (white background bar with colored fill)
canvas = tk.Canvas(root, width=300, height=20, bg="#ffffff", highlightthickness=0)
canvas.pack(pady=(0, 20))

root.mainloop()