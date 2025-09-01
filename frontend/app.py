import tkinter as tk
from calendar import day_abbr
from dbm import error
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
        """User registration form"""
        for widget in self.root.winfo_children():
            widget.destroy()

        signup_frame=ttk.Frame(self.root,padding=20)
        signup_frame.grid(row=0,column=0,sticky=(tk.W,tk.E,tk.S,tk.N))

        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        signup_frame.columnconfigure(1,weight=1)

        #Title
        label=ttk.Label(signup_frame,text="Create New Account",font=("Arial",14))
        label.grid(row=0,column=0,columnspan=2,pady=20)

        #Email field
        ttk.Label(signup_frame,text="Email:").grid(row=1,column=0,sticky=tk.W,pady=5)
        self.signup_email=ttk.Entry(signup_frame,width=30)
        self.signup_email.grid(row=1,column=1,padx=10,pady=5,sticky=tk.EW)

        #password field
        ttk.Label(signup_frame,text="Password:").grid(row=2,column=0,sticky=tk.W,pady=5)
        self.signup_password=ttk.Entry(signup_frame,width=30,show="*")
        self.signup_password.grid(row=2,column=1,padx=10,pady=5,sticky=tk.EW)

        #Confirm password field
        ttk.Label(signup_frame,text="Confirm Password").grid(row=3,column=0,sticky=tk.W,pady=5)
        self.signup_confirm=ttk.Entry(signup_frame,width=30,show="*")
        self.signup_confirm.grid(row=3,column=1,padx=10,pady=5,sticky=tk.EW)


        #Buttons
        signup_btn=ttk.Button(signup_frame,text="sign Up",command=self.signup)
        signup_btn.grid(row=4,column=0,pady=10)

        back_btn=ttk.Button(signup_frame,text="back to Login",command=self.show_login_frame)
        back_btn.grid(row=4,column=1,pady=10)


    def signup(self):
        """Handle user registration"""
        email=self.signup_email.get()
        password=self.signup_password.get()
        confirm=self.signup_confirm.get()

        if not email or not password:
            messagebox.showwarning("Warning","Email and password are required")
            return
        if password!=confirm:
            messagebox.showwarning("Warning","Password do not match")
            return
        try:
            response=requests.post(f"{self.base_url}/signup",
                                   json={"email":email,
                                         "password":password})

            data = response.json()

            if response.status_code==200:
                messagebox.showinfo("Success", data.get("message", "Account created successfully! Please login."))
                self.show_login_frame()
            else:
                error_message = self.extract_error_message(data)
                messagebox.showerror("Error", error_message)


        except Exception as e:
            messagebox.showerror("Error",f"Failed to create account: {str(e)}")


    def extract_error_message(self,data):
        """Extract user friendly error message"""
        #1.Check for fastAPI validation errors
        if isinstance(data.get("detail"),list):
            for error in data["detail"]:
                if "msg" in error:
                    #Extract user-friendly part of msg
                    msg=error["msg"]
                    if "value is not a valid email address:" in msg:
                        return "Please enter a valid email address with a proper domain(e.g., example@gmail.com)"
                    return msg


        if "detail" in data:
            return data["detail"]
        if "message" in data:
            return data["message"]
        return "Failed to create account. Please try again."

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

        self.load_expenses()
        #NEW methods for expense operations
    def add_expense(self):
        """add new expense via API"""
        try:
            amount=self.amount_entry.get()
            category=self.category_entry.get()
            note=self.note_entry.get()

            if not amount or not category:
                messagebox.showwarning("warning","Amount and category are required")
                return
            headers={"Authorization":f"Bearer {self.access_token}"}
            data={
                "amount":float(amount),
                "category":category,
                "note":note
            }
            response=requests.post(f"{self.base_url}/expense",json=data,headers=headers)

            if response.status_code==200:
                #Clear form fields
                self.amount_entry.delete(0,tk.END)
                self.category_entry.delete(0,tk.END)
                self.note_entry.delete(0,tk.END)

                #Refresh expenses list
                self.load_expenses()
                messagebox.showinfo("success","Expense added successfully")

            else:
                messagebox.showerror("Error","Failed to add expense")

        except ValueError:
            messagebox.showerror("Error","Amount must be a number")

        except Exception as e:
            messagebox.showerror("Error",f"Failed to add expense: {str(e)}")





    def delete_expense(self):
        """Delete the selected expense"""
        selected=self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning","please select an expense to delete")
            return
        expense_id=self.tree.item(selected[0])["values"][0]

        try:
            headers={"Authorization":f"Bearer {self.access_token}"}
            response=requests.delete(f"{self.base_url}/expense/{expense_id}",headers=headers)

            if response.status_code==200:
                self.load_expenses()
                messagebox.showinfo("Success","Expense deleted successfully")
            else:
                messagebox.showerror("Error","Failed to delete expense")
        except Exception as e:
            messagebox.showerror("Error",f"Failed to delete expense {str(e)}")


    def load_expenses(self):
        """fetch and display expenses from API"""
        try:
            headers={"Authorization":f"Bearer {self.access_token}"}
            response=requests.get(f"{self.base_url}/expenses",headers=headers)
            if response.status_code==200:
                #Clear existing items in tree view
                for item in self.tree.get_children():
                    self.tree.delete(item)

                #Add expenses to treeview
                expenses=response.json().get("expenses",[])
                for expense in expenses:
                    self.tree.insert("","end",values=(
                        expense["id"],
                        expense['amount'],
                        expense["category"],
                        expense["note"],
                        expense["date"]
                    ))

            else:
                messagebox.showerror("Error","Failed to load expenses")

        except Exception as e:
            messagebox.showerror("Error",f"Failed to load expenses: {str(e)}")

    def logout(self):
        """Logout and return to login screen"""
        self.access_token=None
        self.current_user=None
        self.show_login_frame()

if __name__=="__main__":
    root=tk.Tk()
    app=ExpenseTrackerApp(root)
    root.mainloop()
