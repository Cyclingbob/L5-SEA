from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from config import view_path

systemRouter = APIRouter()
templates = Jinja2Templates(directory=view_path)

@systemRouter.get("/system/{system_id}")
async def sendSystem(system_id: int, request: Request):
    db = request.app.state.db # So we can interact with the database
    system = db.getSystem(system_id)

    if isinstance(system, str): # Failure happened
        if system == "notfound":
            raise HTTPException(status_code=404) # Send the request to 404 page handler (not found)
        else:
            context = { "request": request, "current_user": request.current_user, "error": system } # system will contain error relayed from DB
            return templates.TemplateResponse("500.html", context)
        
    all_components = db.getAllComponents()
    if isinstance(all_components, str): # Error occured
        all_components = []

    linked_system_components = db.getAllSystemComponents(system_id)

    if isinstance(linked_system_components, str):  # normalise DB "notfound" / error cases
        linked_system_components = []

    linked_map = { lsc["component_id"]: lsc["id"] for lsc in linked_system_components } # many to many, so need a map
    
    linked_map = {}
    for lsc in linked_system_components:
        comp_id = lsc.get("component_id")
        if comp_id is None:
            continue
        linked_map.setdefault(comp_id, []).append(lsc.get("id"))

    system_components = []
    for component in all_components:
        comp_id = component.get("id")
        linked_ids = linked_map.get(comp_id, [])
        # append one entry per linked system-component so duplicates show up
        for linked_id in linked_ids:
            comp_copy = component.copy()  # avoid mutating the master list
            comp_copy["linked_system"] = linked_id
            system_components.append(comp_copy)

    belongs_to_project = db.getProject(system["project_id"])

    connections = db.getSystemConnections(system_id)

    if isinstance(connections, str):
        connections = []

    for i, connection in enumerate(connections): # for each connection
        foundA = False
        foundB = False
        looped = False

        while (not foundA or not foundB) and not looped: # Need to find the component for each system component in their connection
            for sc in system_components:
                if sc["linked_system"] == connection["component_a"]:
                    connections[i]["component_a_name"] = sc["name"] # we already linked system component and component together further up here ^
                    foundA = True

                if sc["linked_system"] == connection["component_b"]:
                    connections[i]["component_b_name"] = sc["name"] # we already linked system component and component together further up here ^
                    foundB = True
            looped = True

    system_file_path = "system.html"
    context = { "request": request, "current_user": request.current_user, "system": system, "len": len, "system_project": belongs_to_project, "all_components": all_components, "system_components": system_components, "system_connections": connections }
    return templates.TemplateResponse(system_file_path, context)

class NewSystemCredentials(BaseModel):
    name: str
    category: str
    description: str
    project_id: str

@systemRouter.post("/create-system") # credentials will be JSON encoded
async def createSystem(request: Request, credentials: NewSystemCredentials):
    db = request.app.state.db # So we can interact with the database

    result = db.createSystem(credentials.name, credentials.category, credentials.description, credentials.project_id) # returns ID of new system

    if isinstance(result, int):
        response = JSONResponse(
            status_code=200,
            content={"success": True, "id": result }
        )
    elif result == "duplicate":
        response = JSONResponse(
            status_code=400,
            content={"success": False, "error": "A system with that name already exists!" }
        )
    else:
        response = JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )

    return response

class RenameSystemPayload(BaseModel):
    name: str

@systemRouter.patch("/system/{system_id}/rename")
async def renameSystem(system_id: int, request: Request, namePayload: RenameSystemPayload):
    db = request.app.state.db # So we can interact with the database
    system = db.getSystem(system_id)

    if isinstance(system, str): # Failure happened
        if system == "notfound":
            raise HTTPException(status_code=404) # Send the request to 404 page handler (not found)
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + system }
            )
    
    result = db.editSystem(system_id, namePayload.name, system["category"], system["description"], system["project_id"])
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

class ChangeSystemDescPayload(BaseModel):
    description: str

@systemRouter.patch("/system/{system_id}/description")
async def changeSystemDesc(system_id: int, request: Request, descPayload: ChangeSystemDescPayload):
    db = request.app.state.db # So we can interact with the database
    system = db.getSystem(system_id)

    if isinstance(system, str): # Failure happened
        if system == "notfound":
            raise HTTPException(status_code=404) # Send the request to 404 page handler (not found)
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + system }
            )
    
    result = db.editSystem(system_id, system["name"], system["category"], descPayload.description, system["project_id"])
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

class ChangeSystemCategoryPayload(BaseModel):
    category: str

@systemRouter.patch("/system/{system_id}/category")
async def changeSystemCategory(system_id: int, request: Request, categoryPayload: ChangeSystemCategoryPayload):
    db = request.app.state.db # So we can interact with the database
    system = db.getSystem(system_id)

    if isinstance(system, str): # Failure happened
        if system == "notfound":
            raise HTTPException(status_code=404) # Send the request to 404 page handler (not found)
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + system }
            )
    
    result = db.editSystem(system_id, system["name"], categoryPayload.category, system["description"], system["project_id"])
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

@systemRouter.delete("/system/{system_id}")
async def changeSystemDesc(system_id: int, request: Request):
    db = request.app.state.db # So we can interact with the database
    system = db.getSystem(system_id)
    if isinstance(system, str): # Failure happened
        if system == "notfound":
            raise HTTPException(status_code=404) # Send the request to 404 page handler (not found)
        else:
            response = JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + system }
            )
    
    result = db.deleteSystem(system_id)
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

@systemRouter.post("/system/{system_id}/add-component/{component_id}")
async def addComponentToSystem(system_id: int, component_id: int, request: Request):
    db = request.app.state.db # So we can interact with the database
    system = db.getSystem(system_id)

    if isinstance(system, str): # Failure happened
        if system == "notfound":
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "System not found" }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + system }
            )
    
    component = db.getComponent(component_id)

    if isinstance(component, str): # Failure happened
        if system == "notfound":
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "Component not found" }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + component }
            )
    
    result = db.createSystemComponent(system_id, component_id)
    if isinstance(result, str):
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )
    else:
        return JSONResponse(
            status_code=200,
            content={"success": True }
        )
    
@systemRouter.delete("/system/remove-component/{system_component_id}")
async def deleteSystemComponent(system_component_id: int, request: Request):
    db = request.app.state.db # So we can interact with the database
    system_component = db.getSystemComponent(system_component_id)

    if isinstance(system_component, str): # Failure happened
        if system_component == "notfound":
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "System Component not found" }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + system_component }
            )
        
    result = db.deleteSystemComponent(system_component_id)

    if result != "success":
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )
    else:
        return JSONResponse(
            status_code=200,
            content={"success": True }
        )
    
@systemRouter.get("/system-components/{system_id}.json")    
async def sendSystemComponents(request: Request, system_id: int):
    db = request.app.state.db # So we can interact with the database
    
    components = db.getAllSystemComponents(system_id)
    
    if isinstance(components, str):
        return JSONResponse(
            status_code=500,
            content={ "success": False, "error": "Server error: " + components }
        )

    return JSONResponse(
        status_code=200,
        content={ "success": True, "system_components": components }
    )

class CreateConnectionPayload(BaseModel):
    system_component_a: str
    system_component_b: str
    component_a_label: str
    component_b_label: str

@systemRouter.post("/connection")
async def createConnection(request: Request, connection_payload: CreateConnectionPayload):
    db = request.app.state.db # So we can interact with the database

    componentA = db.getSystemComponent(connection_payload.system_component_a)

    if isinstance(componentA, str): # Failure happened
        if componentA == "notfound":
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "Connection A not found" }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + componentA }
            )

    componentB = db.getSystemComponent(connection_payload.system_component_b)

    if isinstance(componentB, str): # Failure happened
        if componentB == "notfound":
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "Connection B not found" }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + componentB }
            )
        
    if componentA["system_id"] != componentB["system_id"]:
        return JSONResponse(
            status_code=400, # Bad request
            content={"success": False, "error": "Cannot create a system component between two systemms!" }
        )

    result = db.createConnection(connection_payload.system_component_a, connection_payload.system_component_b, connection_payload.component_a_label, connection_payload.component_b_label)

    if isinstance(result, str): # error occured.
        return JSONResponse(
            status_code=500,
            content={ "success": False, "error": "Server error: " + result }
        )
    else:
        return JSONResponse(
            status_code=200,
            content={ "success": True, "id": result }
        )
    
@systemRouter.delete("/connection/{connection_id}")
async def deleteSystemConnection(connection_id: int, request: Request):
    db = request.app.state.db # So we can interact with the database
    connection = db.getConnection(connection_id)

    if isinstance(connection, str): # Failure happened
        if connection == "notfound":
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "Connection not found" }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "Server error: " + connection }
            )
        
    result = db.deleteConnection(connection_id)

    if result != "success":
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Server error: " + result }
        )
    else:
        return JSONResponse(
            status_code=200,
            content={"success": True }
        )
