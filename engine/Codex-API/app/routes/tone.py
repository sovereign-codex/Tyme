from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def broadcast_tone():
    return {"status": "ToneScript activated"}
