from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from app.routers import notes,auth


app = FastAPI()

@app.exception_handler(Exception) # Universal Error handler
async def universal_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
            "error": str(exc)
        }
    )

@app.get("/")
async def root():
    return {"status": "ok"}

app.include_router(notes.router,prefix='/api')
app.include_router(auth.router,prefix='/api')

