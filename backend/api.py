from fastapi import FastAPI,HTTPException,Depends,Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,EmailStr
from typing import Optional,List
import uvicorn
from main import ExpenseDatabase,AuthDatabase
import uuid

#create FastAPI
app=FastAPI(
    title="Expense Tracker API",
    description="API for managing personal expenses with multi-user support",
    version="1.0.0"
)

#Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #In production , specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#pydantic models for request/response
class ExpenseCreate(BaseModel):
    amount:float
    category: str
    note:Optional[str]=None


class UserSignUp(BaseModel):
    email:EmailStr
    password:str

class UserSignIn(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:str
    email:str

#Dependency to get user from authorization header
async def get_current_user(authorization:Optional[str]=Header(None)):
    if not authorization:
        raise HTTPException(status_code=401,detail="Authorization header missing")
    try:
        #Extract token fron bearer token
        token=authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization

        user_result=AuthDatabase.get_user(token)
        if not user_result["success"]:
            raise HTTPException(status_code=401,detail=user_result["message"])

        return user_result["user"]
    except Exception as e:
        raise HTTPException(status_code=401,detail="Invalid authorization token")

#Root end point
@app.get("/")
async def root():
    return {
        "message":"Expense Tracker API",
        "version":"1.0.0",
        "endpoints":["/signup","/login","/me"],
        "expenses":["/expense","/expenses"]
    }

#Authentication Endpoints
@app.post("/signup")
async def signup(user_data:UserSignUp):
    """create a new user account"""
    result=AuthDatabase.sign_up(user_data.email,user_data.password)

    if result["success"]:
        return {
            "success": True,
            "message":result["message"],
            "user":{
                "id":result["user"].id,
                "email":result["user"].email
            }
        }
    else:
        raise HTTPException(status_code=400,detail=result["message"])

@app.post("/login")
async def login(user_data:UserSignIn):
    """login user and return access token"""
    result=AuthDatabase.sign_in(user_data.email,user_data.password)

    if result["success"]:
        return {
            "success":True,
            "message":result["message"],
            "access_token":result["access_token"],
            "user":{
                "id":result["user"].id,
                "email":result["user"].email
            }
        }
    else:
        raise HTTPException(status_code=401,detail=result["message"])

@app.get("/me")
async def get_me(current_user=Depends(get_current_user)):
    """Get current user information"""
    return {
        "success":True,
        "user":{
            "id":current_user.id,
            "email":current_user.email
        }
    }

@app.post("/logout")
async def logout():
    """Logout current user"""
    result=AuthDatabase.sign_out()
    return {
        "success":result["success"],
        "message":result["message"]
    }

@app.post("/expense")
async def add_expense(expense: ExpenseCreate,current_user=Depends(get_current_user)):
    """Add a new expense for a authenticated user"""
    result=ExpenseDatabase.add_expense(
        user_id=current_user.id,
        amount=expense.amount,
        category=expense.category,
        note=expense.note
    )

    if result["success"]:
        return {
            "success":True,
            "message":result["message"],
            "expense":result["data"]
        }
    else:
        raise HTTPException(status_code=400,detail=result["message"])

@app.get("/expenses")
async def get_expenses(current_user=Depends(get_current_user)):
    """Get all expenses for the authenticated user"""
    result=ExpenseDatabase.get_expenses(current_user.id)

    if result["success"]:
        return {
            "success":True,
            "message":result["message"],
            "expenses":result["data"]
        }
    else:
        raise HTTPException(status_code=400,detail=result["message"])

@app.get("/expense/{expense_id}")
async def get_expense(expense_id:str,current_user=Depends(get_current_user)):
    """Get a specific expense by ID"""
    result=ExpenseDatabase.get_expense_by_id(expense_id,current_user.id)

    if result["success"]:
        return {
            "success":True,
            "message":result["message"],
            "expense":result["data"]
        }

    else:
        raise HTTPException(status_code=404,detail=result["message"])

@app.delete("/expense/{expense_id}")
async def delete_expense(expense_id:str,current_user=Depends(get_current_user)):
    """Delete an expense by ID"""
    result=ExpenseDatabase.delete_expense(expense_id,current_user.id)

    if result["success"]:
        return {
            "success":True,
            "message":result["message"]
        }
    else:
        raise HTTPException(status_code=404,detail=result["message"])

#Health checkpoint
@app.get("/health")
async def health_check():
    """Check if the API is running"""
    return {"status":"healthy","message":"API is running successfully"}

#run the app
if __name__ == '__main__':
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )