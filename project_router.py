from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from config import view_path

projectRouter = APIRouter()
templates = Jinja2Templates(directory=view_path)

@projectRouter.get("/project/{project_id}")
async def sendProject(project_id: int, request: Request):
    db = request.app.state.db # So we can interact with the database
    project = db.getProject(project_id)

    if isinstance(project, str): # Failure happened
        if project == "notfound":
            raise HTTPException(status_code=404) # Send the request to 404 page handler (not found)
        else:
            context = { "request": request, "current_user": request.current_user, "error": project } # Project will contain error relayed from DB
            return templates.TemplateResponse("500.html", context)
    
    project_systems = db.getProjectSystems(project_id)
    if project_systems == "notfound":
        project_systems = []

    project_users = db.getProjectUsers(project_id)
    if isinstance(project_users, str):
        project_users = []

    project_owner = db.getUser(project["owner"])
    if isinstance(project_owner, str):
        project_owner = {
            "first_name": "?",
            "surname": "?",
            "email": "?",
            "id": ""
        }
    
    all_users = db.getAllUsers()

    allocated_ids = set()
    for pu in project_users:
        if isinstance(pu, dict):
            allocated_ids.add(pu.get("user_id") or pu.get("id"))

    non_allocated = [
        u for u in all_users
        if u.get("id") != project_owner.get("id") and u.get("id") not in allocated_ids
    ]

    project_file_path = "project.html"
    context = { "request": request, "current_user": request.current_user, "project": project, "all_project_systems": project_systems, "len": len, "project_users": project_users, "project_owner": project_owner, "non_project_users": non_allocated }
    return templates.TemplateResponse(project_file_path, context)

class NewProjectCredentials(BaseModel):
    name: str
    category: str
    description: str

@projectRouter.post("/create-project") # credentials will be JSON encoded
async def createProject(request: Request, credentials: NewProjectCredentials):
    db = request.app.state.db # So we can interact with the database

    result = db.createProject(credentials.name, credentials.category, credentials.description, request.current_user["id"]) # returns ID of new project

    if isinstance(result, int):
        response = JSONResponse(
            status_code=200,
            content={"success": True, "id": result }
        )
    elif result == "duplicate":
        response = JSONResponse(
            status_code=400,
            content={"success": False, "error": "A project with that name already exists!" }
        )
    else:
        response = JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )

    return response

class RenameProjectPayload(BaseModel):
    name: str

@projectRouter.patch("/project/{project_id}/rename")
async def renameProject(project_id: int, request: Request, namePayload: RenameProjectPayload):

    current_user = getattr(request, "current_user", None)
    if not current_user["isAdmin"]: # this endpoint requires administrator permission
        return JSONResponse(
            status_code=403,
            content={"success": False, "error": "Forbidden. Requires administrator permissions." }
        )

    db = request.app.state.db # So we can interact with the database
    project = db.getProject(project_id)

    if isinstance(project, str): # Failure happened
        if project == "notfound":
            response = JSONResponse(
                status_code=404,
                content={"success": False, "error": "Project not found: " + project }
            )
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + project }
            )
    
    result = db.editProject(project_id, namePayload.name, project["category"], project["description"])
    if result == "success":
        response = JSONResponse(
            status_code=200,
            content={"success": True, "name": namePayload.name }
        )
    else:
        response = JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )

    return response

class ChangeProjectDescPayload(BaseModel):
    description: str

@projectRouter.patch("/project/{project_id}/description")
async def changeProjectDesc(project_id: int, request: Request, descPayload: ChangeProjectDescPayload):

    current_user = getattr(request, "current_user", None)
    if not current_user["isAdmin"]: # this endpoint requires administrator permission
        return JSONResponse(
            status_code=403,
            content={"success": False, "error": "Forbidden. Requires administrator permissions." }
        )

    db = request.app.state.db # So we can interact with the database
    project = db.getProject(project_id)

    if isinstance(project, str): # Failure happened
        if project == "notfound":
            response = JSONResponse(
                status_code=404,
                content={"success": False, "error": "Project not found: " + project }
            )
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + project }
            )
    
    result = db.editProject(project_id, project["name"], project["category"], descPayload.description)
    if result == "success":
        response = JSONResponse(
            status_code=200,
            content={"success": True, "description": descPayload.description }
        )
    else:
        response = JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )

    return response

class ChangeProjectCategoryPayload(BaseModel):
    category: str

@projectRouter.patch("/project/{project_id}/category")
async def changeProjectCategory(project_id: int, request: Request, categoryPayload: ChangeProjectCategoryPayload):

    current_user = getattr(request, "current_user", None)
    if not current_user["isAdmin"]: # this endpoint requires administrator permission
        return JSONResponse(
            status_code=403,
            content={"success": False, "error": "Forbidden. Requires administrator permissions." }
        )

    db = request.app.state.db # So we can interact with the database
    project = db.getProject(project_id)

    if isinstance(project, str): # Failure happened
        if project == "notfound":
            response = JSONResponse(
                status_code=404,
                content={"success": False, "error": "Project not found: " + project }
            )
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + project }
            )
    
    result = db.editProject(project_id, project["name"], categoryPayload.category, project["description"])
    if result == "success":
        response = JSONResponse(
            status_code=200,
            content={"success": True, "category": categoryPayload.category }
        )
    else:
        response = JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )

    return response

@projectRouter.delete("/project/{project_id}")
async def deletePrject(project_id: int, request: Request):

    current_user = getattr(request, "current_user", None)
    if not current_user["isAdmin"]: # this endpoint requires administrator permission
        return JSONResponse(
            status_code=403,
            content={"success": False, "error": "Forbidden. Requires administrator permissions." }
        )

    db = request.app.state.db # So we can interact with the database
    project = db.getProject(project_id)

    if isinstance(project, str): # Failure happened
        if project == "notfound":
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "Project not found: " + project }
            )
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + project }
            )
    
    result = db.deleteProject(project_id)
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

class AddUserProjectPayload(BaseModel):
    role: str

@projectRouter.post("/project/{project_id}/add-user/{user_id}")
async def addUserToProject(project_id: int, user_id: int, rolePayload: AddUserProjectPayload, request: Request):

    current_user = getattr(request, "current_user", None)
    if not current_user["isAdmin"]: # this endpoint requires administrator permission
        return JSONResponse(
            status_code=403,
            content={"success": False, "error": "Forbidden. Requires administrator permissions." }
        )

    db = request.app.state.db # So we can interact with the database
    project = db.getProject(project_id)

    if isinstance(project, str): # Failure happened
        if project == "notfound":
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "Project not found: " + project }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + project }
            )
        
    user = db.getUser(project_id)
        
    if isinstance(user, str): # Failure happened
        if user == "notfound":
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "User not found: " + user }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + user }
            )
    
    result = db.createUserProject(user_id, project_id, rolePayload.role)

    if result == "success":
        return JSONResponse(
            status_code=200,
            content={"success": True }
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )
    
@projectRouter.delete("/project/{project_id}/del-user/{user_id}")
async def addUserToProject(project_id: int, user_id: int, request: Request):

    current_user = getattr(request, "current_user", None)
    if not current_user["isAdmin"]: # this endpoint requires administrator permission
        return JSONResponse(
            status_code=403,
            content={"success": False, "error": "Forbidden. Requires administrator permissions." }
        )

    db = request.app.state.db # So we can interact with the database
    project = db.getProject(project_id)

    if isinstance(project, str): # Failure happened
        if project == "notfound":
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "Project not found: " + project }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + project }
            )
        
    user = db.getUser(project_id)
        
    if isinstance(user, str): # Failure happened
        if user == "notfound":
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "User not found: " + user }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + user }
            )
    
    result = db.deleteUserProject(user_id, project_id)

    if result == "success":
        return JSONResponse(
            status_code=200,
            content={"success": True }
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )