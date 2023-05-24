from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.mount("/static", StaticFiles(directory="frontend/dist/static"), name="static")


templates = Jinja2Templates(directory="frontend/dist")
@app.get("/")
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

