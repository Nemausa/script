from tkinter import *


def btnClick():
    textLabel['text'] = '我点击了按钮'


root = Tk(className="Nemausa")
root.geometry("1000x500")

textLabel = Label(root, text='提示显示', justify=LEFT, padx=10, pady=20,width=100, height=20)
textLabel.pack(side=TOP)

# btn = Button(root, text='提示显示', justify=LEFT, padx=20, pady=20)
# btn['text'] = '点击测试'
# btn['command'] = btnClick


mainloop()

