from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import problem_a, problem_b
from routers import mcp_server          # <-- NEW


app = FastAPI(title="My Unified API", lifespan=mcp_server.mcp_app.lifespan)

# CORS — required for the grader's browser page
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["mcp-session-id"],
)

app.include_router(problem_a.router)
app.include_router(problem_b.router)
# --- NEW: mount MCP at /mcp ---




@app.get("/")
def root():
    return {"message": "Unified API is running"}
app.mount("/", mcp_server.mcp_app)
# UV set up 
# uv init # INITIALIZE PROJECT
# uv add fastapi uvicorn json5
# uv run uvicorn main:app --reload # RUNNING APP