import tkinter as tk
import time

# -----------------------------
# Geometry Dash Wave Spam Game
# -----------------------------

class WaveSpamChallenge:
    def __init__(self, root):
        self.root = root
        self.root.title("GD Wave Spam Challenge 🌊")
        self.root.geometry("500x400")
        self.root.configure(bg="black")

        self.score = 0
        self.time_limit = 5
        self.running = False

        # Title
        self.title_label = tk.Label(
            root,
            text="🌊 WAVE SPAM CHALLENGE 🌊",
            font=("Arial", 20, "bold"),
            fg="cyan",
            bg="black"
        )
        self.title_label.pack(pady=20)

        # Score Display
        self.score_label = tk.Label(
            root,
            text="Waves: 0",
            font=("Arial", 18),
            fg="white",
            bg="black"
        )
        self.score_label.pack()

        # Timer Display
        self.timer_label = tk.Label(
            root,
            text="Time: 5",
            font=("Arial", 18),
            fg="yellow",
            bg="black"
        )
        self.timer_label.pack(pady=10)

        # Instructions
        self.info_label = tk.Label(
            root,
            text="Spam SPACE as fast as possible!",
            font=("Arial", 14),
            fg="lime",
            bg="black"
        )
        self.info_label.pack(pady=15)

        # Start Button
        self.start_button = tk.Button(
            root,
            text="START CHALLENGE",
            font=("Arial", 14, "bold"),
            bg="purple",
            fg="white",
            command=self.start_game
        )
        self.start_button.pack(pady=20)

        # Result Label
        self.result_label = tk.Label(
            root,
            text="",
            font=("Arial", 16, "bold"),
            fg="orange",
            bg="black"
        )
        self.result_label.pack(pady=15)

        # Key Binding
        self.root.bind("<space>", self.wave_press)

    # -----------------------------
    # Start Game
    # -----------------------------
    def start_game(self):
        self.score = 0
        self.running = True
        self.start_time = time.time()
        self.result_label.config(text="")
        self.start_button.config(state="disabled")

        self.update_timer()

    # -----------------------------
    # Space Press = Wave Spam
    # -----------------------------
    def wave_press(self, event):
        if self.running:
            self.score += 1
            self.score_label.config(text=f"Waves: {self.score}")

    # -----------------------------
    # Timer Countdown
    # -----------------------------
    def update_timer(self):
        if self.running:
            elapsed = time.time() - self.start_time
            remaining = self.time_limit - int(elapsed)

            if remaining > 0:
                self.timer_label.config(text=f"Time: {remaining}")
                self.root.after(200, self.update_timer)
            else:
                self.end_game()

    # -----------------------------
    # End Game + Rank System
    # -----------------------------
    def end_game(self):
        self.running = False
        self.timer_label.config(text="Time: 0")
        self.start_button.config(state="normal")

        # Ranking
        if self.score < 10:
            rank = "🐢 NOOB WAVER"
        elif self.score < 20:
            rank = "😄 DECENT SPAMMER"
        elif self.score < 35:
            rank = "⚡ WAVE PRO"
        else:
            rank = "🏆 GD WAVE LEGEND"

        self.result_label.config(
            text=f"Final Score: {self.score}\nRank: {rank}"
        )


# -----------------------------
# Run App
# -----------------------------
root = tk.Tk()
game = WaveSpamChallenge(root)
root.mainloop()