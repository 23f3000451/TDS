from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import problem_a, problem_b

app = FastAPI(title="My Unified API")

# CORS — required for the grader's browser page
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(problem_a.router)
app.include_router(problem_b.router)


@app.get("/")
def root():
    return {"message": "Unified API is running"}

# UV set up 
# uv init # INITIALIZE PROJECT
# uv add fastapi uvicorn json5
# uv run uvicorn main:app --reload # RUNNING APP