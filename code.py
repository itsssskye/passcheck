import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
import re

# Settings
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

# Update bar
def on_key_release(event=None):
    pw = entry.get()
    state, score = check_state(pw)
    color = get_color_for_state(state)

    width = progress_canvas.winfo_width()
    fill_width = int((score / max_score) * width)

    progress_canvas.delete("all")

    # Gray BG
    progress_canvas.create_round_rect(0, 0, width, bar_height, radius=15, fill="#f2f2f2", outline="")

    # Colored filled portion
    if fill_width > 0:
        progress_canvas.create_round_rect(0, 0, fill_width, bar_height, radius=15, fill=color, outline="")

    # Text overlay
    text_color = "#fff" if score >= 4 else "#000"
    progress_canvas.create_text(width//2, bar_height//2, text=state, fill=text_color, font=("Segoe UI", 14, "bold"))

# Custom round rect
def round_rect(canvas):
    def _create_round_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
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
        return self.create_polygon(points, smooth=True, splinesteps=36, **kwargs)
    canvas.create_round_rect = _create_round_rect.__get__(canvas)

# Define window size
window_width = 400
window_height = 200

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate position
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the position of the window
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Main frame
main = tb.Frame(root, padding=20)
main.pack(fill="both", expand=True)

# Label
label = tb.Label(main, text="Password:", font=("Segoe UI", 14, "bold"), bootstyle="dark")
label.pack(anchor="w")

# Entry frame w/ shadow
entry_wrapper = tk.Frame(main, bg="white")
entry_wrapper.pack(fill="x", pady=(0, 20))

# Entry
entry = tb.Entry(main, font=("Segoe UI", 14), bootstyle="secondary")
entry.pack(fill="x", padx=4)
entry.focus()
entry.bind("<KeyRelease>", on_key_release)

# Progress bar canvas
progress_canvas = tk.Canvas(main, height=bar_height, bg="white", highlightthickness=0)
round_rect(progress_canvas)
progress_canvas.pack(fill="x", pady=(30, 10))

# Update on resize
def on_resize(event=None):
    on_key_release()

root.bind("<Configure>", on_resize)

# Initial draw
root.after(100, on_key_release)

# Start
root.mainloop()