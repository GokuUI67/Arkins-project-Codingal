import random
from tkinter import *

# Create the main window
root = Tk()
root.title("Rock Paper Scissors")
root.geometry("400x400")
root.config(bg="#E3F2FD")

# Choices
choices = ["Rock", "Paper", "Scissors"]

# Function to play the game
def play(user_choice):
    comp_choice = random.choice(choices)
    result_text = f"Your Choice: {user_choice}\nComputer's Choice: {comp_choice}\n\n"
    
    if user_choice == comp_choice:
        result_text += "It's a Tie!"
    elif (user_choice == "Rock" and comp_choice == "Scissors") or \
         (user_choice == "Paper" and comp_choice == "Rock") or \
         (user_choice == "Scissors" and comp_choice == "Paper"):
        result_text += "🎉 You Win!"
    else:
        result_text += "😢 You Lose!"

    result_label.config(text=result_text)

# Heading
Label(root, text="Rock Paper Scissors", font=("Arial", 18, "bold"), bg="#E3F2FD", fg="#0D47A1").pack(pady=15)

# Instruction
Label(root, text="Choose your move:", font=("Arial", 12), bg="#E3F2FD").pack(pady=5)

# Buttons for Rock, Paper, Scissors
button_frame = Frame(root, bg="#E3F2FD")
button_frame.pack(pady=10)

rock_btn = Button(button_frame, text="🪨 Rock", width=12, height=2, bg="#90CAF9", fg="black", command=lambda: play("Rock"))
paper_btn = Button(button_frame, text="📄 Paper", width=12, height=2, bg="#A5D6A7", fg="black", command=lambda: play("Paper"))
scissors_btn = Button(button_frame, text="✂️ Scissors", width=12, height=2, bg="#FFCC80", fg="black", command=lambda: play("Scissors"))

rock_btn.grid(row=0, column=0, padx=10)
paper_btn.grid(row=0, column=1, padx=10)
scissors_btn.grid(row=0, column=2, padx=10)

# Label to show result
result_label = Label(root, text="", font=("Arial", 12), bg="#E3F2FD", fg="#1A237E", justify=CENTER)
result_label.pack(pady=30)

# Run the window
root.mainloop()