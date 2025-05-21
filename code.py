import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
import re

# Settings
bar_width = 300
bar_height = 30
max_score = 7

# State scoring
def check_state(password):
    score = 0
    length = len(password)

    if length >= 6: score += 1
    if length >= 8: score += 1
    if length >= 12: score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"\d", password): score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): score += 1

    if length == 0: return "Empty", 0
    elif score == 1: return "Extremely Weak", 1
    elif score == 2: return "Very Weak", 2
    elif score == 3: return "Weak", 3
    elif score == 4: return "Fair", 4
    elif score == 5: return "Good", 5
    elif score == 6: return "Strong", 6
    elif score >= 7: return "Extremely Strong", 7
    return "Very Strong", 6

# State colors
def get_color_for_state(state):
    return {
        "Empty": "#bbbbbb",
        "Extremely Weak": "#ff4d4d",
        "Very Weak": "#ff704d",
        "Weak": "#ff9966",
        "Fair": "#ffcc66",
        "Good": "#b3d166",
        "Strong": "#66b366",
        "Very Strong": "#339933",
        "Extremely Strong": "#00cc44",
    }.get(state, "#000000")

# Rounded rectangle
def create_rounded_rect(canvas, x1, y1, x2, y2, radius=10, **kwargs):
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, splinesteps=36, **kwargs)

# Update bar
def on_key_release(event=None):
    pw = entry.get()
    state, score = check_state(pw)
    color = get_color_for_state(state)

    fill_width = int((score / max_score) * bar_width)

    # Clear canvas
    progress_canvas.delete("all")

    # Shadow
    create_rounded_rect(progress_canvas, 2, 2, bar_width+2, bar_height+2, radius=18, fill="#dddddd")

    # Background bar
    create_rounded_rect(progress_canvas, 0, 0, bar_width, bar_height, radius=15, fill="#f0f0f0")

    # Colored filled portion
    if fill_width > 0:
        create_rounded_rect(progress_canvas, 0, 0, fill_width, bar_height, radius=15, fill=color)

    # Text overlay
    text_color = "#fff" if score >= 4 else "#000"
    progress_canvas.create_text(bar_width//2, bar_height//2, text=state, fill=text_color, font=("Segoe UI", 14, "bold"))

# Setup window
root = tb.Window(themename="flatly")
root.title("PassCheck")
root.geometry("400x250")
root.resizable(False, False)
root.configure(bg="white")
main_frame = tb.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

# Password label
label = tb.Label(main_frame, text="Password:")
label.pack(anchor="w", padx=40, pady=(20, 0))
label.configure(font=("Segoe UI", 14, "bold"))

# Entry with shadow
entry_frame = tk.Canvas(main_frame, width=320, height=45, bg="white", highlightthickness=0)
entry_frame.pack()
create_rounded_rect(entry_frame, 3, 3, 320, 45, radius=18, fill="#aaaaaa")
create_rounded_rect(entry_frame, 0, 0, 320, 45, radius=18, fill="#ffffff")

# Real entry
entry = tb.Entry(main_frame, font=("Segoe UI", 12))
entry.place(x=55, y=88)
entry.focus()
entry.bind("<KeyRelease>", on_key_release)

# Progress bar canvas
progress_canvas = tk.Canvas(main_frame, width=bar_width, height=bar_height, bg="white", highlightthickness=0)
progress_canvas.pack(pady=30)

# Initial draw
on_key_release()

# Run app
root.mainloop()