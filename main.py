from fastapi import FastAPI 
from fastapi.responses import JSONResponse
from users.routes import router as guest_router, user_router
from auth.routes import router as auth_router
from starlette.middleware.authentication import AuthenticationMiddleware
from users.services import JWTAuth


app = FastAPI(debug=True)
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)
# app.include_router(refresh_router)

# Add Middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())


@app.get('/')
def status_check():
    return JSONResponse(content={"status": "Running!"})