from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/{glyph_id}")
def get_glyph(glyph_id: str):
    return JSONResponse(content={"glyph_id": glyph_id, "type": "fractal", "coherence": 0.99})
