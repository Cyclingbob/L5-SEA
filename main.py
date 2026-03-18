import uvicorn

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import Database

from authenciate_user import AuthenticateUserMiddleware
from login_router import loginRouter
from project_router import projectRouter
from system_router import systemRouter
from componentRouter import componentRouter
from user_router import userRouter

from config import public_path, view_path, database_file, port

app = FastAPI()
app.state.db = Database(database_file)
templates = Jinja2Templates(directory=view_path)

app.mount("/public", StaticFiles(directory=public_path), name="public")
app.add_middleware(AuthenticateUserMiddleware)
app.include_router(loginRouter)
app.include_router(projectRouter)
app.include_router(systemRouter)
app.include_router(componentRouter)
app.include_router(userRouter)

@app.get("/")
def read_root(request: Request):
    current_user = getattr(request, "current_user", None)
    db = app.state.db

    all_projects = db.getAllProjects()
    if isinstance(all_projects, str): # Error occured
        all_projects = [
            {
                "name": "Error occured",
                "category": "",
                "description": all_projects,
                "id": ""
            }
        ]

    owned_projects = []
    for project in all_projects:
        print
        if project["owner"] == current_user["id"]:
            owned_projects.append(project)

    current_user = getattr(request, "current_user", None)
    user_id = current_user.get("id") if isinstance(current_user, dict) else getattr(current_user, "id", None)

    user_projects = db.getUserProjects(user_id)
    if isinstance(user_projects, str): # Error occured
        user_projects = []
    
    context = { "request": request, "current_user": request.current_user, "user_projects": user_projects, "owned_projects": owned_projects, "len": len }
    return templates.TemplateResponse("index.html", context)

@app.get("/admin")
def render_administrator_page(request: Request):
    current_user = getattr(request, "current_user", None)
    db = app.state.db

    if not current_user["isAdmin"]:
        context = { "request": request, "current_user": current_user, "all_projects": [], "len": len }
        return templates.TemplateResponse("403.html", context)

    all_projects = db.getAllProjects()
    if isinstance(all_projects, str): # Error occured
        all_projects = [
            {
                "name": "Error occured",
                "category": "",
                "description": all_projects,
                "id": ""
            }
        ]

    all_users = db.getAllUsers()
    if isinstance(all_users, str):
        if all_users == "notfound":
            all_users = {
                "first_name": "error",
                "surname": "",
                "email": "No users found",
                "isAdmin": False,
                "id": ""
            }
        else:
            all_users = {
                "first_name": "error",
                "surname": "",
                "email": all_users,
                "isAdmin": False,
                "id": ""
            }

    context = { "request": request, "current_user": request.current_user, "all_projects": all_projects, "all_users": all_users, "len": len } # Needed for Jinja logic
    return templates.TemplateResponse("administrator.html", context)

@app.exception_handler(404)
async def not_found_handler(request: Request, exception):
    context = { "request": request, "current_user": request.current_user }
    return templates.TemplateResponse("404.html", context)

if __name__ == "__main__":
    uvicorn.run(app, port=port)