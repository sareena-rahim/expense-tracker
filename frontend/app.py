import tkinter as tk
from calendar import day_abbr
from tkinter import ttk,messagebox
import requests

class ExpenseTrackerApp:
    def __init__(self,root):
        self.root=root
        self.root.title("Expense Tracker")
        self.root.geometry("400x400")
        self.current_user=None
        self.access_token=None
        self.base_url="http://localhost:8000"

        self.show_login_frame()
    def show_login_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        #Login frame
        login_frame=ttk.Frame(self.root,padding="20")
        login_frame.grid(row=0,column=0,sticky=(tk.W,tk.E,tk.N,tk.S))

        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        login_frame.columnconfigure(1,weight=1)


        label=ttk.Label(login_frame,text="Expense Tracker Login",font=("Arial",14))
        label.grid(row=0,column=0,columnspan=2,pady=20)

        #email field
        ttk.Label(login_frame,text="Email:").grid(row=1,column=0,sticky=tk.W,pady=5)
        self.email_entry=ttk.Entry(login_frame,width=30)
        self.email_entry.grid(row=1,column=1,padx=10,pady=5,sticky=tk.EW)

        #password field
        ttk.Label(login_frame,text="Password:").grid(row=2,column=0,pady=5,sticky=tk.W)
        self.password_entry=ttk.Entry(login_frame,width=30,show="*")
        self.password_entry.grid(row=2,column=1,padx=10,pady=5,sticky=tk.EW)
        #login button
        login_btn=ttk.Button(login_frame,text="Login",command=self.login)
        login_btn.grid(row=3,column=0,pady=10)

        #sign up button
        signup_btn=ttk.Button(login_frame,text="Sign Up",command=self.show_signup_frame)
        signup_btn.grid(row=3,column=1,pady=10)


        #API test button
        test_btn=ttk.Button(login_frame,text="Test API connection",command=self.test_api_connection)
        test_btn.grid(row=4,column=0,columnspan=2,pady=20)


    def test_api_connection(self):
        try:
            response=requests.get(f"{self.base_url}/health")
            if response.status_code ==200:
                messagebox.showinfo("Success","API is connected and working")
            else:
                messagebox.showerror("Error",f"API returned status {response.status_code}")
        except Exception as e:
            messagebox.showerror("Connection Error",f"Cannot connect to API:\n{str(e)}")

    def login(self):
        email=self.email_entry.get()
        password=self.password_entry.get()

        try:
            response=requests.post(f"{self.base_url}/login",
                                   json={"email":email,"password":password})


            if response.status_code==200:
                data=response.json()
                self.access_token=data["access_token"]
                self.current_user=data["user"]

                messagebox.showinfo("Success", f"Welcome back, {data['user']['email']}!")
                self.show_main_app()

            else:
                messagebox.showerror("Error","Login failed")

        except Exception as e:
            messagebox.showerror("Error",f"Connection error : {str(e)}")




    def show_signup_frame(self):
        """place holder for signup"""
        messagebox.showinfo("Info","Signup frame will be implemented")

if __name__=="__main__":
    root=tk.Tk()
    app=ExpenseTrackerApp(root)
    root.mainloop()
