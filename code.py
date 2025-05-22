import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout,
    QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QColor, QFont
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


# Main Window
class PasswordChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PassCheck")
        self.setFixedSize(420, 250)
        self.setStyleSheet("background-color: white;")

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Label
        self.label = QLabel("Password:")
        self.label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.label.setStyleSheet("color: #333333;")
        layout.addWidget(self.label)

        # Entry shadow wrapper
        self.entry_shadow = QFrame()
        self.entry_shadow.setStyleSheet("background-color: white; border-radius: 10px;")
        self.entry_shadow.setFixedHeight(40)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.entry_shadow.setGraphicsEffect(shadow)
        layout.addWidget(self.entry_shadow)

        # Entry
        self.entry = QLineEdit()
        self.entry.setFont(QFont("Segoe UI", 14))
        self.entry.setPlaceholderText("Enter password...")
        self.entry.setStyleSheet("""
            QLineEdit {
                border: none;
                padding: 8px;
                background-color: white;
                border-radius: 10px;
            }
        """)
        entry_layout = QVBoxLayout(self.entry_shadow)
        entry_layout.setContentsMargins(10, 0, 10, 0)
        entry_layout.addWidget(self.entry)

        self.entry.textChanged.connect(self.update_bar)

        # Bar shadow wrapper
        self.bar_wrapper = QFrame()
        self.bar_wrapper.setFixedHeight(bar_height)
        self.bar_wrapper.setStyleSheet("background-color: #f2f2f2; border-radius: 15px;")
        bar_shadow = QGraphicsDropShadowEffect()
        bar_shadow.setBlurRadius(15)
        bar_shadow.setOffset(0, 4)
        bar_shadow.setColor(QColor(0, 0, 0, 30))
        self.bar_wrapper.setGraphicsEffect(bar_shadow)
        layout.addWidget(self.bar_wrapper)

        # Bar fill
        self.bar_fill = QFrame(self.bar_wrapper)
        self.bar_fill.setStyleSheet("background-color: #bbbbbb; border-radius: 15px;")
        self.bar_fill.setGeometry(0, 0, 0, bar_height)

        # Text overlay
        self.state_label = QLabel(self.bar_wrapper)
        self.state_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.state_label.setStyleSheet("color: #000000;")
        self.state_label.setGeometry(0, 0, self.bar_wrapper.width(), bar_height)

    # Update the bar
    def update_bar(self):
        password = self.entry.text()
        state, score = check_state(password)
        color = get_color_for_state(state)

        width = self.bar_wrapper.width()
        fill_width = int((score / max_score) * width)

        self.bar_fill.setGeometry(0, 0, fill_width, bar_height)
        self.bar_fill.setStyleSheet(f"background-color: {color}; border-radius: 15px;")

        text_color = "#ffffff" if score >= 4 else "#000000"
        self.state_label.setText(state)
        self.state_label.setStyleSheet(f"color: {text_color}; font-weight: bold;")


# Start
app = QApplication(sys.argv)
window = PasswordChecker()
window.show()
sys.exit(app.exec())