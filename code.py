import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout,
    QGraphicsDropShadowEffect, QFrame
)
from PyQt6.QtGui import QColor, QPainter, QFont
from PyQt6.QtCore import Qt


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

# Main widget
class PasswordStrengthApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PassCheck")
        self.resize(400, 200)
        self.setStyleSheet("background-color: white;")

        # Main frame
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Label
        label = QLabel("Password:")
        label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        label.setStyleSheet("color: #333;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Entry w/ shadow
        self.entry = QLineEdit()
        self.entry.setFont(QFont("Segoe UI", 14))
        self.entry.setPlaceholderText("Enter your password...")
        self.entry.setStyleSheet("""
            QLineEdit {
                background-color: #f9f9f9;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        self.entry.textChanged.connect(self.update_bar)

        # Shadow for entry
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.entry.setGraphicsEffect(shadow)

        layout.addWidget(self.entry)

        # Progress bar frame w/ shadow
        self.bar_frame = QFrame()
        self.bar_frame.setFixedHeight(bar_height)
        self.bar_frame.setStyleSheet("""
            QFrame {
                background-color: #f2f2f2;
                border-radius: 15px;
            }
        """)

        # Shadow for progress bar
        self.bar_shadow = QGraphicsDropShadowEffect(self)
        self.bar_shadow.setBlurRadius(15)
        self.bar_shadow.setXOffset(0)
        self.bar_shadow.setYOffset(4)
        self.bar_shadow.setColor(QColor(0, 0, 0, 50))
        self.bar_frame.setGraphicsEffect(self.bar_shadow)

        layout.addWidget(self.bar_frame)

        # Text overlay
        self.state_label = QLabel("")
        self.state_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.state_label)

        # Initial values
        self.score = 0
        self.color = "#bbbbbb"

        # Start
        self.show()

    # Update bar
    def update_bar(self):
        pw = self.entry.text()
        state, self.score = check_state(pw)
        self.color = get_color_for_state(state)
        self.state_label.setText(state)
        text_color = "#fff" if self.score >= 4 else "#000"
        self.state_label.setStyleSheet(f"color: {text_color};")
        self.repaint()

    # Custom paint for filled portion
    def paintEvent(self, event):
        super().paintEvent(event)
        rect = self.bar_frame.geometry()
        if rect.width() == 0: return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(self.color))
        painter.setPen(Qt.PenStyle.NoPen)

        fill_width = int((self.score / max_score) * rect.width())
        if fill_width > 0:
            painter.drawRoundedRect(rect.x(), rect.y(), fill_width, rect.height(), 15, 15)

# Run app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    root = PasswordStrengthApp()

    # Define window size
    window_width = 400
    window_height = 200

    # Get screen width and height
    screen_width = app.primaryScreen().size().width()
    screen_height = app.primaryScreen().size().height()

    # Calculate position
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set the position of the window
    root.move(x, y)

    sys.exit(app.exec())