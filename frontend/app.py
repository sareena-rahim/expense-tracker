import tkinter as tk
from tkinter import ttk,messagebox
import requests

class ExpenseTrackerApp:
    def __init__(self,root):
        self.root=root
        self.root.title("Expense Tracker")
        self.root.geometry("400x300")
        self.current_user=None
        self.access_token=None
        self.base_url="http://localhost:8000"

        self.show_login_frame()
    def show_login_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        #Login frame
        login_frame=ttk.Frame(self.root,padding="20")
        login_frame.pack(fill=tk.BOTH,expand=True)

        label=ttk.Label(login_frame,text="Expense Tracker Login",font=("Arial",14))
        label.pack(pady=20)

        #API test button
        test_btn=ttk.Button(login_frame,text="Test API connection",command=self.test_api_connection)
        test_btn.pack(pady=20)


    def test_api_connection(self):
        try:
            response=requests.get(f"{self.base_url}/health")
            if response.status_code ==200:
                messagebox.showinfo("Success","API is connected and working")
            else:
                messagebox.showerror("Error",f"API returned status {response.status_code}")
        except Exception as e:
            messagebox.showerror("Connection Error",f"Cannot connect to API:\n{str(e)}")


if __name__=="__main__":
    root=tk.Tk()
    app=ExpenseTrackerApp(root)
    root.mainloop()
