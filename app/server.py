
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import uvicorn

api = FastAPI(title="Synthetic Soul Assistant")

from .metrics_exporter import router as metrics_router
api.include_router(metrics_router)

from .workspace import app as workspace_app
from .magic_rect import magic_rect

class ChatRequest(BaseModel):
    text:str

class ChatResponse(BaseModel):
    text:str

@api.post("/chat",response_model=ChatResponse)
def chat(req:ChatRequest):
    try:
        output=workspace_app.invoke({"text":req.text})
        return ChatResponse(text=output.get("text",""))
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@api.get("/magic-rect")
def magic_rect_view():
    return {"matrix":magic_rect.matrix()}

if __name__=="__main__":
    uvicorn.run(api,host="0.0.0.0",port=8000)
