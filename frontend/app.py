import tkinter as tk
from tkinter import ttk

class ExpenseTrackerApp:
    def __init__(self,root):
        self.root=root
        self.root.title("Expense Tracker")
        self.root.geometry("400x300")
        self.current_user=None
        self.access_token=None
        self.basic_url="http://localhost:8000"

        self.show_login_frame()
    def show_login_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        label=ttk.Label(self.root,text="Expense Tracker Login")
        label.pack(pady=20)
        



if __name__=="__main__":
    root=tk.Tk()
    app=ExpenseTrackerApp(root)
    root.mainloop()
