from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/")
async def complete(request: Request):
    body = await request.json()
    prompt = body.get("input", "")
    # Placeholder logic: integrate AVOT-core here
    return {
        "output": f"AVOT response to: '{prompt}'",
        "source": "Codex-API"
    }
