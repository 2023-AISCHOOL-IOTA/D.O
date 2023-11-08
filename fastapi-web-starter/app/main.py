from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import datetime
from .library.helpers import *
from app.routers import twoforms, unsplash, accordion


app = FastAPI()


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(unsplash.router)
app.include_router(twoforms.router)
app.include_router(accordion.router)


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})

@app.get("/")
async def home(request: Request):
    return {"message":"success"}



@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


@app.get("/model")
async def home(request: Request):
    # Bert = None
    # output = Bert("이것은 입력입니다.")
    return {"message":"success", "data": "이것은 출력입니다."}


@app.get("/hello")
async def home(request: Request):
    now = datetime.datetime.now()
    return templates.TemplateResponse("page.html", {"request": request, "now": now})
    # return {"message":"success"}