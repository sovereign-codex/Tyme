from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def save_scroll():
    return {"message": "Scroll registered (stub)"}
