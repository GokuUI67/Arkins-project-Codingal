from tkinter import *
from tkinter import messagebox
from PIL import image, ImageTk
root = Tk()
root.title("The Denomination Calculator")
root.configure(bg= 'light blue')
root.geometry("650x400")
upload = image.open("app_img.jpg")
upload = upload.resize((300, 300))
image = ImageTk.PhotoImage(upload)
label = Label(root, image=image, bg= 'light blue')
label.place(x=180, y=20)
label1 = Label(root,
               text="Hey User! Welcome to The Denomination Counter Application!",
               bg= 'light blue')
label1.place(relx=0.5, y=340, anchor=CENTER)
def msg():
    MsgBox =messagebox.showinfo(
        "!ALERT!", "Do You Want To Calculate The Denomination Count?")
    if MsgBox == 'ok':
        topwin()
button1 = Button(root,
                 text="Let's Get Started!",
                 command=msg,
                 bg='brown',
                 fg='white',)
button1.place(x=260, y=360)