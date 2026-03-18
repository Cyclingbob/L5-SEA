from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

class AuthenticateUserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/login"):
            return await call_next(request)
        
        if request.url.path.startswith("/signup"):
            return await call_next(request)
        
        if request.url.path.startswith("/public"):
            return await call_next(request)
        
        db = request.app.state.db
    
        session_cookie = request.cookies.get("session")
    
        if not session_cookie:
            return RedirectResponse("/login")
    
        user = db.getUser(session_cookie)
        
        if user == "notfound":
            return RedirectResponse("/login")
     
        Request.current_user = user

        response = await call_next(request)
        return response