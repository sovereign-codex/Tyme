from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def spawn_hivelet():
    return {"message": "Hivelet spawned (stub)"}
