import os
from supabase import create_client,Client
from dotenv import load_dotenv
from typing import List,Dict,Optional

#load environment variables
load_dotenv()

#Supabase configuration
SUPABASE_URL=os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY=os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY=os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("Missing supabase credentials in .env")

#create supabase client
supabase:Client=create_client(SUPABASE_URL,SUPABASE_ANON_KEY)

# service role client (needed for admin actions like auto-confirm)
supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

class ExpenseDatabase:
    """Handles all database operations"""

    @staticmethod
    def add_expense(user_id:str,amount:float,category:str,note:str=None):
        """Add new expenses to the database"""
        try:
            expense_data={
                "user_id":user_id,
                "amount":amount,
                "category":category,
                "note":note
            }

            result=supabase.table("expenses").insert(expense_data).execute()

            if result.data:
                return {
                    "success":True,
                    "data":result.data[0],
                    "message":"Expense added successfully"
                }
            else:
                return {
                    "success":False,
                    "message":"Failed to add expense"
                }
        except Exception as e:
            return {
                "success":False,
                "message":f"Error adding expense: {str(e)}"

            }

    @staticmethod
    def get_expenses(user_id:str):
        """Get all expenses for a specific user"""
        try:
            result=supabase.table("expenses").select("*").eq("user_id",user_id).order("date",desc=True).execute()

            return {
                "success":True,
                "data":result.data,
                "message":f"found{len(result.data)} expenses"
            }
        except Exception as e:
            return {
                "success":False,
                "message":f"Error fetching expenses: {str(e)}",
                "data":[]
            }

    @staticmethod
    def delete_expense(expense_id:str,user_id:str):
        """Delete an expense (only if it belong to the user)"""

        try:
            result=supabase.table("expenses").delete().eq("id",expense_id).eq("user_id",user_id).execute()

            if result.data:
                return {
                    "success":True,
                    "message":"Expense deleted successfully"
                }
            else:
                return {
                    "success":False,
                    "message":"Expense not found or not authorized to delete"
                }

        except Exception as e:
            return {
                "success":False,
                "message":f'Error deleting expense:{str(e)}'
            }

    @staticmethod
    def get_expense_by_id(expense_id:str,user_id:str):
        """Get specific expense by ID"""
        try:
            result=supabase.table("expenses").select("*").eq("id",expense_id).eq("user_id",user_id).execute()
            if result.data:
                return {
                    "success":True,
                    "data":result.data[0],
                    "message":"Expense found"
                }
            else:
                return {
                    "success":False,
                    "message":"Expense not found"
                }
        except Exception as e:
            return {
                "success":False,
                "message":f'Error fetching expense:{str(e)}'
            }
class AuthDatabase:
    """Handles authentication operation"""

    @staticmethod
    def sign_up(email:str,password:str):
        """create a new user account"""
        try:
            result=supabase.auth.sign_up({
                "email":email,
                "password":password
            })


            if result.user:
                supabase_admin.auth.admin.update_user_by_id(
                    result.user.id,
                    {"email_confirmed": True}
                )


                return {
                    "success":True,
                    "user":result.user,
                    "message":"User created successfully (auto-confirmed)"
                }

            error_message = result.error.message if result.error else "Signup failed. Please try again."
            return {
                "success": False,
                "message": error_message
            }


        except Exception as e:
            error_msg = str(e).lower()
            if "already registered" in error_msg or "user already registered" in error_msg:
                return {
                    "success": False,
                    "message": "This email is already registered. Please log in instead."
                }
            else:
                return {
                    "success": False,
                    "message": error_msg
                }

    @staticmethod
    def sign_in(email:str,password:str):
        """Sign in an existing user"""
        try:
            result=supabase.auth.sign_in_with_password({
                "email":email,
                "password":password
            })
            if result.user and result.session:
                return {
                    "success":True,
                    "user":result.user,
                    "session":result.session,
                    "access_token":result.session.access_token,
                    "message":"Login successful"
                }
            else:
                return {
                    "success":False,
                    "message":"Invalid credentials"
                }

        except Exception as e:
            return {
                "success":False,
                "message":f"Error sign in {str(e)}"
            }

    @staticmethod
    def get_user(access_token:str):
        """Get user details from access token"""
        try:
            #set the session with access token
            supabase.auth.set_session(access_token,refresh_token="")

            user= supabase.auth.get_user(access_token)

            if user:
                return {
                    "success":True,
                    "user":user.user,
                    "message":"user retrieved successfully"
                }
            else:
                return {
                    "success":False,
                    "message":"Invalid token"
                }
        except Exception as e:
            return {
                "success":False,
                "message":f"Error getting user: {str(e)}"
            }
    @staticmethod
    def sign_out():
        """sign out to current user"""
        try:
            supabase.auth.sign_out()
            return {
                "success":True,
                "message":"Signed out successfully"
            }
        except Exception as e:
            return {
                "success":False,
                "Message":f"Error signing out{str(e)}"
            }

# Test function to verify connection
def test_connection():
    """Test the Supabase connection"""
    try:
        # Try to fetch from expenses table (will return empty if no data)
        result = supabase.table("expenses").select("*").limit(1).execute()
        print("✅ Supabase connection successful!")
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

if __name__ == "__main__":
    # Test the connection
    test_connection()