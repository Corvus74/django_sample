from fastapi import FastAPI
from api.controllers import router as api_router
from sample.controllers import router as sample_router

# Define the server configuration for Swagger UI
# This helps Swagger UI make requests to the correct base URL, especially behind a proxy.
servers = [
    {
        "url": "/",
        "description": "Default Server (for local development or direct access)"
    },
    {
        "url": "/api",
        "description": "API Server (when accessed via /api prefix)"
    }
]

app = FastAPI(
    title="Project API",
    root_path="/api", # Keep root_path for correct internal URL generation
    servers=servers # Add the servers configuration for Swagger UI
)

app.include_router(api_router)
app.include_router(sample_router, prefix="/sample")
