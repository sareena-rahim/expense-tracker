import tkinter as tk
from calendar import day_abbr
from tkinter import ttk,messagebox
import requests

class ExpenseTrackerApp:
    def __init__(self,root):
        self.root=root
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")
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



    def show_main_app(self):
        #clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        #create main frame
        main_frame=ttk.Frame(self.root,padding=20)
        main_frame.grid(row=0,column=0,sticky=(tk.W,tk.E,tk.N,tk.S))

        #configure responsive layout
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        main_frame.columnconfigure(1,weight=1)


        #welcome message
        welcome_label=ttk.Label(main_frame,text=f"Welcome, {self.current_user['email']}!")
        welcome_label.grid(row=0,column=0,columnspan=3,pady=10)

        #Expense list
        columns=("ID","Amount","Category","Note","Date")
        self.tree=ttk.Treeview(main_frame,columns=columns,show="headings",height=10)


        #Define headings
        self.tree.heading("ID",text="ID")
        self.tree.heading("Amount",text="Amount")
        self.tree.heading("Category",text="Category")
        self.tree.heading("Note",text="Note")
        self.tree.heading("Date",text="Date")

        #Set column width
        self.tree.column("ID",width=50)
        self.tree.column("Amount",width=80)
        self.tree.column("Category",width=100)
        self.tree.column("Note",width=150)
        self.tree.column("Date",width=120)

        self.tree.grid(row=1,column=0,columnspan=3,pady=10,sticky=(tk.W,tk.E,tk.N,tk.S))


        #Add expense form
        ttk.Label(main_frame,text="Add New Expense",font=("Arial",12,"bold")).grid(
            row=2,column=0,columnspan=3,pady=10,sticky=tk.W)

        #Amount
        ttk.Label(main_frame,text="Amount:").grid(row=3,column=0,sticky=tk.W,pady=5)
        self.amount_entry=ttk.Entry(main_frame,width=15)
        self.amount_entry.grid(row=3,column=1,pady=5,sticky=tk.W)

        #category
        ttk.Label(main_frame,text="Category:").grid(row=4,column=0,sticky=tk.W,pady=5)
        self.category_entry=ttk.Entry(main_frame,width=15)
        self.category_entry.grid(row=4,column=1,pady=5,sticky=tk.W)

        #Note
        ttk.Label(main_frame,text="Note:").grid(row=5,column=0,sticky=tk.W,pady=5)
        self.note_entry=ttk.Entry(main_frame,width=15)
        self.note_entry.grid(row=5,column=1,pady=5,sticky=tk.W)

        #Action buttons
        add_button=ttk.Button(main_frame,text="Add Expense",command=self.add_expense)
        add_button.grid(row=6,column=0,pady=10,padx=5)

        delete_btn=ttk.Button(main_frame,text="Delete Selected",command=self.delete_expense)
        delete_btn.grid(row=6,column=1,pady=10,padx=5)

        logout_btn=ttk.Button(main_frame,text="Logout",command=self.logout)
        logout_btn.grid(row=6,column=2,pady=10,padx=5)

        refresh_btn=ttk.Button(main_frame,text="Refresh",command=self.load_expenses)
        refresh_btn.grid(row=7,column=0,pady=5,columnspan=3)


        #NEW methods for expense operations
    def add_expense(self):
        """for add expense"""
        messagebox.showinfo("Info","Add expense functionality will be implemented")

    def delete_expense(self):
        """for delete expense"""
        messagebox.showinfo("Info","Delete expense functionality will be implemented")

    def load_expenses(self):
        """for load expense"""
        messagebox.showinfo("Info","Load expense functionality will be implemented")

    def logout(self):
        """Logout and return to login screen"""
        self.access_token=None
        self.current_user=None
        self.show_login_frame()

if __name__=="__main__":
    root=tk.Tk()
    app=ExpenseTrackerApp(root)
    root.mainloop()
