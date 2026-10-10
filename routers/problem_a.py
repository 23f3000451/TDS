from fastapi import APIRouter

router = APIRouter(prefix="/problem-a", tags=["Problem A"])

@router.get("/hello")
def hello_a():
    return {"message": "Hello from Problem A"}