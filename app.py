from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from api.api_v1 import api_v1
import uvicorn
from middlewares.auth_middleware import AuthMiddleWare
# Removed unused import: from fastapi_utils.tasks import repeat_every
from db.session import SessionLocal
 # Adjusted import to use relative path


root_router = APIRouter()
app = FastAPI()

app.add_middleware(AuthMiddleWare)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@root_router.get("/")
def hello_world():
    return {"message": "Hello World!"}


app.include_router(api_v1.route_v1)
app.include_router(root_router)


# ✅ Custom OpenAPI for Swagger Authorize Button
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="API with JWT token via middleware",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if "security" not in openapi_schema["paths"][path][method]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
