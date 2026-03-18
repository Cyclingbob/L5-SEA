from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from config import view_path

componentRouter = APIRouter()
templates = Jinja2Templates(directory=view_path)

@componentRouter.get("/components")
async def sendComponents(request: Request):
    db = request.app.state.db # So we can interact with the database
    
    components = db.getAllComponents()
    if isinstance(components, str):
        context = { "request": request, "current_user": request.current_user, "error": components } # component will contain error relayed from DB
        return templates.TemplateResponse("500.html", context)

    project_file_path = "components.html"
    context = { "request": request, "current_user": request.current_user, "all_components": components, "len": len }
    return templates.TemplateResponse(project_file_path, context)

@componentRouter.get("/components.json")
async def sendComponents(request: Request):
    db = request.app.state.db # So we can interact with the database
    
    components = db.getAllComponents()
    
    if isinstance(components, str):
        return JSONResponse(
            status_code=500,
            content={ "success": False, "error": "Server error: " + components }
        )

    return JSONResponse(
        status_code=200,
        content={ "success": True, "components": components }
    )

@componentRouter.get("/component/{component_id}")
async def sendComponent(component_id: int, request: Request):
    db = request.app.state.db # So we can interact with the database
    component = db.getComponent(component_id)

    if isinstance(component, str): # Failure happened
        if component == "notfound":
            raise HTTPException(status_code=404) # Send the request to 404 page handler (not found)
        else:
            context = { "request": request, "current_user": request.current_user, "error": component } # component will contain error relayed from DB
            return templates.TemplateResponse("500.html", context)

    component_file_path = "component.html"
    context = { "request": request, "current_user": request.current_user, "component": component, "len": len }
    return templates.TemplateResponse(component_file_path, context)

class NewComponentCredentials(BaseModel):
    name: str
    type: str
    part_number: str
    unit_cost: float

@componentRouter.post("/component") # credentials will be JSON encoded
async def createComponent(request: Request, credentials: NewComponentCredentials):
    db = request.app.state.db # So we can interact with the database

    result = db.createComponent(credentials.name, credentials.type, credentials.part_number, credentials.unit_cost) # returns ID of new component

    if isinstance(result, int):
        response = JSONResponse(
            status_code=200,
            content={"success": True, "id": result }
        )
    elif result == "duplicate":
        response = JSONResponse(
            status_code=400,
            content={"success": False, "error": "A component with that name already exists!" }
        )
    else:
        response = JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )

    return response

class RenameComponentPayload(BaseModel):
    name: str

@componentRouter.patch("/component/{component_id}/rename")
async def renameComponent(component_id: int, request: Request, namePayload: RenameComponentPayload):
    db = request.app.state.db # So we can interact with the database
    component = db.getComponent(component_id)

    if isinstance(component, str): # Failure happened
        if component == "notfound":
            raise HTTPException(status_code=404) # Send the request to 404 page handler (not found)
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + component }
            )
    
    result = db.editComponent(component_id, namePayload.name, component["type"], component["part_number"], component["unit_cost"])
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

class ChangeComponentTypePayload(BaseModel):
    type: str

@componentRouter.patch("/component/{component_id}/type")
async def changeComponentType(component_id: int, request: Request, typePayload: ChangeComponentTypePayload):
    db = request.app.state.db # So we can interact with the database
    component = db.getComponent(component_id)

    if isinstance(component, str): # Failure happened
        if component == "notfound":
            raise HTTPException(status_code=404) # Send the request to 404 page handler (not found)
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + component }
            )
    
    result = db.editComponent(component_id, component["name"], typePayload.type, component["part_number"], component["unit_cost"])
    if result == "success":
        response = JSONResponse(
            status_code=200,
            content={"success": True, "type": typePayload.type }
        )
    else:
        response = JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )

    return response

class ChangeComponentPartNumberPayload(BaseModel):
    part_number: str

@componentRouter.patch("/component/{component_id}/part-number")
async def changeComponentPartNumber(component_id: int, request: Request, pnPayload: ChangeComponentPartNumberPayload):
    db = request.app.state.db # So we can interact with the database
    component = db.getComponent(component_id)

    if isinstance(component, str): # Failure happened
        if component == "notfound":
            raise HTTPException(status_code=404) # Send the request to 404 page handler (not found)
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + component }
            )
    
    result = db.editComponent(component_id, component["name"], component["type"], pnPayload.part_number, component["unit_cost"])
    if result == "success":
        response = JSONResponse(
            status_code=200,
            content={"success": True, "part_number": pnPayload.part_number }
        )
    else:
        response = JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )

    return response

class ChangeComponentUnitCostPayload(BaseModel):
    unit_cost: float

@componentRouter.patch("/component/{component_id}/unit-cost")
async def changeUnitCost(component_id: int, request: Request, ucPayload: ChangeComponentUnitCostPayload):
    db = request.app.state.db # So we can interact with the database
    component = db.getComponent(component_id)

    if isinstance(component, str): # Failure happened
        if component == "notfound":
            raise HTTPException(status_code=404) # Send the request to 404 page handler (not found)
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + component }
            )
    
    result = db.editComponent(component_id, component["name"], component["type"], component["part_number"], ucPayload.unit_cost)
    if result == "success":
        response = JSONResponse(
            status_code=200,
            content={"success": True, "unit_cost": ucPayload.unit_cost }
        )
    else:
        response = JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )

    return response

@componentRouter.delete("/component/{component_id}")
async def deleteComponent(component_id: int, request: Request):

    current_user = getattr(request, "current_user", None)
    if not current_user["isAdmin"]: # this endpoint requires administrator permission
        return JSONResponse(
            status_code=403,
            content={"success": False, "error": "Forbidden. Requires administrator permissions." }
        )

    examples_in_use = db.getComponentUsed(component_id)
    if len(examples_in_use) > 0:

        examples = set()
        system_ids = []
        for ex in examples_in_use:
            sid = ex.get("system_id")
            if sid is None:
                continue # we don't want to cause a fatal error, gracefully ignore and loop on
            if sid not in examples:
                examples.add(sid)
                system_ids.append(sid)

        return JSONResponse(
            status_code=403,
            content={"success": False, "error": "Forbidden. Used on project(s) " + ",".join(system_ids) + ". Remove before deleting." }
        )

    db = request.app.state.db # So we can interact with the database
    component = db.getComponent(component_id)

    if isinstance(component, str): # Failure happened
        if component == "notfound":
            raise HTTPException(status_code=404) # Send the request to 404 page handler (not found)
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + component }
            )
    
    result = db.deleteComponent(component_id)
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