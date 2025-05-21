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

# Strength colors
def get_color_for_strength(strength):
    colors = {
        "Empty": "#bbbbbb",              # Light gray
        "Extremely Weak": "#ff4d4d",     # Red
        "Very Weak": "#ff704d",          # Orange-Red
        "Weak": "#ff9966",               # Orange
        "Fair": "#ffcc66",               # Yellow-Orange
        "Good": "#b3d166",               # Yellow-Green
        "Strong": "#66b366",             # Greenish
        "Very Strong": "#339933",        # Dark Green
        "Extremely Strong": "#00cc44",  # Bright Green
    }
    return colors.get(strength, "#000000")

# Rounded rectangle on canvas helper
def create_rounded_rect(canvas, x1, y1, x2, y2, radius=10, **kwargs):
    points = [
        x1+radius, y1,
        x1+radius, y1,
        x2-radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1+radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

# Update progress bar & overlay text
def on_key_release(event=None):
    pw = entry.get()
    result, score = check_strength(pw)
    color = get_color_for_strength(result)

    max_score = 7
    bar_width = 300
    bar_height = 30

    # Clear canvas
    progress_canvas.delete("all")

    # Draw shadow (offset rounded rect)
    create_rounded_rect(progress_canvas, 5, 5, bar_width+5, bar_height+5, radius=15, fill="#aaa")

    # Draw background rounded bar (white)
    create_rounded_rect(progress_canvas, 0, 0, bar_width, bar_height, radius=15, fill="#fff")

    if len(pw) > 0:
        fill_width = int((score / max_score) * bar_width)
        # Draw fill bar with rounded edges
        if fill_width > 0:
            create_rounded_rect(progress_canvas, 0, 0, fill_width, bar_height, radius=15, fill=color)

    # Overlay strength text in center
    progress_canvas.create_text(bar_width//2, bar_height//2, text=result, fill="#fff" if score >= 4 else "#000", font=("Segoe UI", 14, "bold"))

# Setup main window
root = tk.Tk()
root.title("PassCheck")
root.configure(bg="#ffffff")

# Center window
window_width = 400
window_height = 220
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Shadow for label "Password:"
label_shadow = tk.Label(root, text="Password:", font=("Segoe UI", 16), bg="#aaa", fg="#888")
label_shadow.place(x=102, y=30)

label = tk.Label(root, text="Password:", font=("Segoe UI", 16), bg="#fff", fg="#222")
label.place(x=100, y=28)

# Canvas for entry background with shadow
entry_canvas = tk.Canvas(root, width=320, height=40, bg="#fff", highlightthickness=0)
entry_canvas.place(x=40, y=60)
create_rounded_rect(entry_canvas, 0, 0, 320, 40, radius=15, fill="#fff")
# Shadow behind entry
entry_shadow = tk.Canvas(root, width=320, height=40, bg="#aaa", highlightthickness=0)
entry_shadow.place(x=45, y=65)
create_rounded_rect(entry_shadow, 0, 0, 320, 40, radius=15, fill="#aaa")

# Entry widget (no password hiding)
entry = tk.Entry(root, font=("Segoe UI", 16), width=30, bd=0, relief="flat", justify="center")
entry.place(x=50, y=70)
entry.focus()
entry.bind("<KeyRelease>", on_key_release)

# Progress bar canvas
progress_canvas = tk.Canvas(root, width=300, height=30, bg="#fff", highlightthickness=0)
progress_canvas.place(x=50, y=120)

# Initial draw
on_key_release()

root.mainloop()