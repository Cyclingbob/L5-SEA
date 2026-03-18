from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from config import view_path
from database import hashPassword

userRouter = APIRouter()
templates = Jinja2Templates(directory=view_path)

@userRouter.get("/user/{user_id}")
async def sendUser(user_id: int, request: Request):
    db = request.app.state.db # So we can interact with the database
    user = db.getUser(user_id)

    if isinstance(user, str): # Failure happened
        if user == "notfound":
            raise HTTPException(status_code=404) # Send the request to 404 page handler (not found)
        else:
            context = { "request": request, "current_user": request.current_user, "error": user } # Project will contain error relayed from DB
            return templates.TemplateResponse("500.html", context)

    context = { "request": request, "current_user": request.current_user, "user": user, "len": len }
    return templates.TemplateResponse("user.html", context)

class NewUserCredentials(BaseModel):
    first_name: str
    surname: str
    email: str
    password: str

@userRouter.post("/create-user") # user credentials will be JSON encoded. Creates a new user
async def createUser(request: Request, userCredentials: NewUserCredentials):

    current_user = getattr(request, "current_user", None)
    if not current_user["isAdmin"]: # this endpoint requires administrator permission
        return JSONResponse(
            status_code=403,
            content={"success": False, "error": "Forbidden. Requires administrator permissions." }
        )

    db = request.app.state.db # So we can interact with the database

    result = db.createUser(userCredentials.first_name, userCredentials.surname, userCredentials.email, userCredentials.password) # returns ID of new project

    if isinstance(result, int):
        response = JSONResponse(
            status_code=200,
            content={"success": True, "id": result }
        )
    else:
        response = JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )

    return response

class renameUserPayload(BaseModel):
    first_name: str
    surname: str

@userRouter.patch("/user/{user_id}/rename")
async def renameUser(user_id: int, request: Request, namePayload: renameUserPayload):

    current_user = getattr(request, "current_user", None)
    if not current_user["isAdmin"]: # this endpoint requires administrator permission
        return JSONResponse(
            status_code=403,
            content={"success": False, "error": "Forbidden. Requires administrator permissions." }
        )

    db = request.app.state.db # So we can interact with the database
    user = db.getUser(user_id)

    if isinstance(user, str): # Failure happened
        if user == "notfound":
            response = JSONResponse(
                status_code=404,
                content={"success": False, "error": "User not found: " + user }
            )
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + user }
            )
    
    result = db.editUser(user_id, namePayload.first_name, namePayload.surname, user["email"], user["password"])
    if result == "success":
        response = JSONResponse(
            status_code=200,
            content={"success": True, "first_name": namePayload.first_name, "surname": namePayload.surname }
        )
    else:
        response = JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )

    return response

class ChangeUserEmailPayload(BaseModel):
    email: str

@userRouter.patch("/user/{user_id}/email")
async def changeUserEmail(user_id: int, request: Request, emailPayload: ChangeUserEmailPayload):

    current_user = getattr(request, "current_user", None)
    if not current_user["isAdmin"]: # this endpoint requires administrator permission
        return JSONResponse(
            status_code=403,
            content={"success": False, "error": "Forbidden. Requires administrator permissions." }
        )

    db = request.app.state.db # So we can interact with the database
    user = db.getUser(user_id)

    if isinstance(user, str): # Failure happened
        if user == "notfound":
            response = JSONResponse(
                status_code=404,
                content={"success": False, "error": "User not found: " + user }
            )
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + user }
            )
    
    result = db.editUser(user_id, user["first_name"], user["surname"], emailPayload.email, user["password"])
    if result == "success":
        response = JSONResponse(
            status_code=200,
            content={"success": True, "email": emailPayload.email }
        )
    else:
        response = JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )

    return response

class ChangeUserPasswordPayload(BaseModel):
    password: str

@userRouter.patch("/user/{user_id}/password")
async def changeUserPassword(user_id: int, request: Request, passwordPayload: ChangeUserPasswordPayload):

    current_user = getattr(request, "current_user", None)
    if not current_user["isAdmin"]: # this endpoint requires administrator permission
        return JSONResponse(
            status_code=403,
            content={"success": False, "error": "Forbidden. Requires administrator permissions." }
        )

    db = request.app.state.db # So we can interact with the database
    user = db.getUser(user_id)

    if isinstance(user, str): # Failure happened
        if user == "notfound":
            response = JSONResponse(
                status_code=404,
                content={"success": False, "error": "User not found: " + user }
            )
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + user }
            )
    
    password = hashPassword(passwordPayload.password)
    result = db.editUser(user_id, user["first_name"], user["surname"], user["email"], password)
    if result == "success":
        response = JSONResponse(
            status_code=200,
            content={"success": True, "password": passwordPayload.password }
        )
    else:
        response = JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )

    return response

@userRouter.delete("/user/{user_id}")
async def deleteUser(user_id: int, request: Request):

    current_user = getattr(request, "current_user", None)
    if not current_user["isAdmin"]: # this endpoint requires administrator permission
        return JSONResponse(
            status_code=403,
            content={"success": False, "error": "Forbidden. Requires administrator permissions." }
        )

    db = request.app.state.db # So we can interact with the database
    user = db.getUser(user_id)

    if isinstance(user, str): # Failure happened
        if user == "notfound":
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "User not found: " + user }
            )
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + user }
            )
    
    result = db.deleteUser(user_id)
    if result == "success":
        response = JSONResponse(
            status_code=200,
            content={"success": True }
        )
    else:
        response = JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )

    return response