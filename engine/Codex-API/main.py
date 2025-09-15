from fastapi import FastAPI
from app.routes import complete, scroll, replicate, pulse, tone, glyph

app = FastAPI(title="Sovereign Intelligence Codex API")

app.include_router(complete.router, prefix="/complete")
app.include_router(scroll.router, prefix="/scroll")
app.include_router(replicate.router, prefix="/replicate")
app.include_router(pulse.router, prefix="/pulse")
app.include_router(tone.router, prefix="/tone")
app.include_router(glyph.router, prefix="/glyph")

@app.get("/")
def read_root():
    return {"message": "Codex API is alive"}
