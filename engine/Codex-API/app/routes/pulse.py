from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def show_pulse():
    return {"pulse": "Field resonance is stable"}
