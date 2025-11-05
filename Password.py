import tkinter as tk
import re
def check_strength(password):
    strength = 0
    remarks = ""
    if len(password) >= 8:
        strength += 1
    if re.search(r"[A-Z]", password):
        strength += 1
    if re.search(r"[a-z]", password):
        strength += 1
    if re.search(r"[0-9]", password):
        strength += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        strength += 1
    if strength <= 2:
        remarks = "Weak 🔴"
    elif strength == 3:
        remarks = "Moderate 🟡"
    elif strength >= 4:
        remarks = "Strong 🟢"
    return remarks
def evaluate():
    pwd = entry.get()
    result = check_strength(pwd)
    label_result.config(text=f"Strength: {result}")
root = tk.Tk()
root.title("🔐 Password Strength Checker")
root.geometry("350x200")
tk.Label(root, text="Enter Password:", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(root, show="*", width=30)
entry.pack()
tk.Button(root, text="Check Strength", command=evaluate).pack(pady=10)
label_result = tk.Label(root, text="", font=("Arial", 12))
label_result.pack()
root.mainloop()