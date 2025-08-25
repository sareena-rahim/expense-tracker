import tkinter as tk
from tkinter import ttk

class ExpenseTrackerApp:
    def __init__(self,root):
        self.root=root
        self.root.title("Expense Tracker")
        self.root.geometry("400x300")


        #Test: Basic window should open
        test_label=ttk.Label(text="Tkinter Working",font=("Arial",16))
        test_label.pack(pady=50)

if __name__=="__main__":
    root=tk.Tk()
    app=ExpenseTrackerApp(root)
    root.mainloop()
