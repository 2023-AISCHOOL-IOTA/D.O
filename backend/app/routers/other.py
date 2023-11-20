from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import APIKeyCookie, APIKeyHeader
#그외 모아둔 라우터
router = APIRouter()


# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates/html")


#  responsebody통해  받아옴 넘어오는 Request는  여기서 request라고 지정
#get방식
@router.get("/")
def read_root(request: Request):
    # HTML 템플릿을 사용하여 렌더링
    return templates.TemplateResponse("home.html", {"request": request})  #이 주소로 요청이 오면 HOME이 열리게

@router.get("/dobot") # 로고 누르면 여기로 요청이 옴 그럼이 HTML이 열림
def read_root(request: Request):
    # HTML 템플릿을 사용하여 렌더링
    
    return templates.TemplateResponse("dobot.html", {"request": request })
