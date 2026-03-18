from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse, FileResponse
from pydantic import BaseModel

from config import view_path

loginRouter = APIRouter()

@loginRouter.get("/login")
async def sendLogin(): # authenticate_user.py middleware checks if user is already logged in.
    login_file_path = view_path + "/login.html"
    return FileResponse(login_file_path, media_type="text/html")

@loginRouter.get("/signup")
async def sendSignup(): # authenticate_user.py middleware checks if user is already logged in.
    signup_file_path = view_path + "/signup.html"
    return FileResponse(signup_file_path, media_type="text/html")

class LoginCredentials(BaseModel):
    email: str
    password: str

@loginRouter.post("/login") # credentials will be JSON encoded
async def login(request: Request, credentials: LoginCredentials):
    db = request.app.state.db # So we can interact with the database
    result = db.login(credentials.email, credentials.password)

    if result == "wrongpassword":
        return JSONResponse(
            status_code=401,
            content={"error": "Incorrect password", "success": False}
        )
    elif result == "notfound":
        return JSONResponse(
            status_code=404,
            content={"error": "User not found", "success": False}
        )
    elif result.startswith("Failed"):
        return JSONResponse(
            status_code=500,
            content={"error": "Login user failed (" + result + ")", "success": False}
        )
    
    user_id = result.split(":")[0]
    
    response = JSONResponse(
        status_code=200,
        content={"success": True}
    )
    # result is username:password
    response.set_cookie(
        key="session",
        value=user_id,
        httponly=True, # Stop JavaScript reading cookie = More Secure
        samesite="lax" # Mitigate CSRF attacks (cross site request forgery)
    )

    return response

class SignupCredentials(BaseModel):
    first_name: str
    surname: str
    email: str
    password: str

@loginRouter.post("/signup")
async def signup(request: Request, credentials: SignupCredentials):
    db = request.app.state.db # So we can interact with the database
    
    exists = db.userExists(credentials.email) # Check if the user already exists (same email)
    if isinstance(exists, str): # Report failure to the user's browser
        return JSONResponse(
            status_code=500,
            content={"error": exists, "success": False}
        )
    elif exists: # User already exists
        return JSONResponse(
            status_code=409,
            content={"error": "User already exists", "success": False}
        )
    else:
        result = db.createUser(credentials.first_name, credentials.surname, credentials.email, credentials.password)
        if result == "success":
            return JSONResponse(
                status_code=201,
                content={"message": "User created successfully", "success": True}
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"error": "Create user failed (" + result + ")", "success": False}
            )

@loginRouter.get("/logout")
async def logout():
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("session")
    return response